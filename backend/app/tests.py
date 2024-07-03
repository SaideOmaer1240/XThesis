import logging
import json
import asyncio
import re
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from asgiref.sync import sync_to_async
from .models import User, Thesis, Topic

logger = logging.getLogger(__name__)

class Esboco:
    def indice(self):
        return ["introdução", "objetivo geral", "objetivo específico", "metodologia", "justificativa"]

    def conclusao(self):
        return ["Conclusão", "Bibliografia"]

User = get_user_model()

class ScribConsumer(AsyncWebsocketConsumer):
    def resposta_em_json(self, indices):
        indices_str = str(indices)
        padrao = r'"([^"]*)"'
        resultado = re.findall(padrao, indices_str)
        return resultado

    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection opened")

    async def receive(self, text_data):
        logger.info('Data received: %s', text_data)

        groq_api_key = settings.GROQ_API_KEY
        llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")

        data = json.loads(text_data)
        tema = data.get('tema', 'tema padrão')
        user_id = data.get('user_id')

        try:
            user = await sync_to_async(User.objects.get)(id=user_id)
            logger.info('User found: %s', user)
        except User.DoesNotExist:
            logger.error('User not found')
            await self.send(text_data=json.dumps({'error': 'Usuário não encontrado'}))
            return

        prompts = {
            "introdução": """Imagine-se redigindo um trabalho escolar sobre um tema crucial: ["{question}"]. ...""",
            "objetivo geral": """Elabore um objetivo geral do tema "{question}": ...""",
            "objetivo específico": """Elabore os objetivos específicos para "{question}": ...""",
            "metodologia": """Apresente qual metodologia usará para elaborar o trabalho sobre "{question}": ...""",
            "justificativa": """Elabore uma justificativa do tema "{question}": ...""",
            "desenvolvimento": """Elaborar um trabalho acadêmico seguindo rigorosamente as diretrizes da APA ...""",
            "bibliografia": """Crie a referência bibliográfica seguindo esse conteúdo context: {context}"""
        }

        prompt_template = """
        Desenvolva um esboço detalhado, criando um índice ou sumário para o trabalho sobre {question}.
        O esboço deve estar em formato de json. A resposta sua deve ser absolutamente apenas o conteúdo em json, não retorne outro tipo de conteúdo antes ou depois de json. As chaves devem ter aspas simples e os valores aspas duplas, por exemplo: 'Título': "Fotossíntese das Plantas".
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        model = llm
        outline_chain = (
            prompt
            | model
            | StrOutputParser()
        )

        try:
            logger.info("Invoking outline chain with question: %s", tema)
            indices = await sync_to_async(outline_chain.invoke)({"question": tema})
            logger.info('Indices received: %s', indices)
            sumario = self.resposta_em_json(indices)
        except Exception as e:
            logger.error('Error in outline chain: %s', e)
            await self.send(text_data=json.dumps({'error': str(e)}))
            return

        indice = Esboco().indice()
        conclusao = Esboco().conclusao()

        for elemento in sumario:
            indice.append(elemento)
        for i in conclusao:
            indice.append(i)

        total_items = len(indice)
        processed_items = 0

        for titulo in indice:
            logger.info('Processing title: %s', titulo)
            if titulo.lower() in prompts:
                prompt_text = prompts[titulo.lower()]
            else:
                prompt_text = prompts["desenvolvimento"]

            linha_de_saida = ChatPromptTemplate.from_template(prompt_text)
            chain = (
                linha_de_saida
                | model
                | StrOutputParser()
            )

            try:
                if titulo.lower() == "bibliografia":
                    response = await sync_to_async(chain.invoke)({"context": "conteúdo de exemplo"})
                else:
                    response = await sync_to_async(chain.invoke)({"question": tema})

                logger.info('Response for %s: %s', titulo, response)

                # Salvar no banco de dados
                await self.save_thesis_content(user, tema, titulo, response)

                await self.send(text_data=json.dumps({
                    'title': titulo,
                    'content': response
                }))

                # Atualizar progresso
                processed_items += 1
                progress = (processed_items / total_items) * 100
                await self.send(text_data=json.dumps({
                    'progress': progress
                }))

            except Exception as e:
                logger.error('Error processing %s: %s', titulo, e)
                await self.send(text_data=json.dumps({'error': str(e)}))

            await asyncio.sleep(30)

    async def disconnect(self, close_code):
        logger.info('WebSocket connection closed with code %s', close_code)

    @sync_to_async
    def save_thesis_content(self, user, tema, titulo, conteudo):
        logger.info('Saving content: %s for user %s', titulo, user)
        # Salvar o tema no banco de dados, se não existir
        topic, created = Topic.objects.get_or_create(author=user, name=tema)
        
        # Salvar o conteúdo gerado no banco de dados
        Thesis.objects.create(author=user, theme=topic, title=titulo, text=conteudo)
        logger.info('Content saved: %s for user %s', titulo, user)
