import logging
import json 
import asyncio
import re   
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer 
from asgiref.sync import sync_to_async
from .models import Thesis
from accounts.models import UserData 
from tools.agents import Escritor, Translator
from learnfetch import Pesquisador
import uuid 

logger = logging.getLogger(__name__)
#pesquisar = Pesquisador()

User = get_user_model()

class ScribConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection opened")

    async def receive(self, text_data):
        logger.info('Data received: %s', text_data)

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.error('Invalid JSON received: %s', e)
            await self.send(text_data=json.dumps({'error': 'Dados JSON inválidos'}))
            return

        user_id = data.get('user_id')

        if user_id:
            user = await self.get_user_by_id(user_id)
            if user:  
                # Obter dados do UserData
                dados = await self.get_userdata(user)
                
                tema = data.get('tema', 'tema padrão')
                institute = data.get('institute', dados.get('instituto'))
                disciplina = data.get('disciplina', dados.get('disciplina'))
                student = data.get('student', dados.get('aluno'))
                instructor = data.get('instructor', dados.get('professor'))
                cidade = data.get('cidade', dados.get('cidade'))
                idioma = data.get('idioma')
                logger.info('Idioma capturado: %s', idioma)
                import time
                time.sleep(5)
                # Identificadores Universalmente Exclusivos
                code =  str(uuid.uuid4()) 

                if not all([tema, user_id, institute, disciplina, student, instructor, cidade]):
                    logger.error('Missing required fields in received data')
                    await self.send(text_data=json.dumps({'error': 'Campos obrigatórios faltando'}))
                    return 
 
                llm = Escritor() 
                translator = Translator() 
                #images = await self.get_image(tema, pesquisar)
                 
                # print(images) 
                content = await self.get_context(code)
                
                if 'Português' in idioma: 
                    
                    topico = tema
                else:
                    topico = translator.translate(tema, idioma) 

                try:
                    logger.info("Invoking outline chain with question: %s", tema)
                    indice = await sync_to_async(llm.generate_index)(lang=idioma, topic=topico)
                    logger.info('Indices received: %s', indice) 
                except Exception as e:
                    logger.error('Error in outline chain: %s', e)
                    await self.send(text_data=json.dumps({'error': str(e)}))
                    return
 
                print(indice)
                total_items = len(indice)
                processed_items = 0 
                
                for i, titulo in enumerate(indice): 
                    logger.info('Processing title: %s', titulo)
                    try:
                        if i == len(indice) - 1:
                            title = f"Desenvolva {titulo} para esse tema: {tema}"
                            response = await sync_to_async(llm.generate_response)(index=indice, lang=idioma, title=title, image_base=content)
                            logger.info('Processo concluido com sucesso da tarefa %s: %s', titulo)
                        else:
                            title = f"Desenvolva somente esse titulo: {titulo}"
                            response = await sync_to_async(llm.generate_response)(index=indice, lang=idioma, title=title, image_base=content)

                            

                        regex = r'<div\b[^>]*>(.*?)<\/div>'
                        resultados = re.findall(regex, response, re.DOTALL)
                        results = ' '.join(resultados) 
                        # Salvar no banco de dados
                        await self.save_thesis_content(user, tema, titulo, results, institute, disciplina, student, instructor, cidade, code)

                        await self.send(text_data=json.dumps({
                            'title': titulo,
                            'content': response,
                            'code': code
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

                    await asyncio.sleep(5)  # Ajustado para reduzir o tempo de espera

               

            else:
                await self.send(text_data=json.dumps({'error': 'Usuário não encontrado'}))
        else:
            await self.send(text_data=json.dumps({'error': 'user_id não fornecido'}))
        
    async def disconnect(self, close_code):
        logger.info('WebSocket connection closed with code %s', close_code)

    @sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @sync_to_async
    def get_image(self, qury : str, engine):
        images = []
        p = engine.get_response(qury) 
        for txt in p:
            txts = txt.get('content', 'Conteúdo não encontrado')
            images.append(txts)
        for i in p:
            img = i.get('img', '')
            alt_regex = r'<img\s[^>]*?alt="([^"]*?)"[^>]*?>'
            url_pattern = re.compile(r'(https?://\S+\.(?:jpg|jpeg|png|gif))')
            url_match = url_pattern.search(img) 
            alt_match = re.search(alt_regex, img)
            if alt_match and url_match:
                alt_text = alt_match.group(1)
                url = url_match.group(0)
                image = f'<img alt ="{alt_text}" src="{url}" style="height: 200px; width: 200px;"/>'
                images.append(image)
            else:
                pass
        return images
        
    @sync_to_async
    def get_userdata(self, user):
        queryset = UserData.objects.filter(author=user).last()
        if queryset:
            return {
                'id': queryset.id,
                'aluno': queryset.aluno,
                'professor': queryset.professor,
                'instituto': queryset.instituto,
                'cidade': queryset.cidade,
                'disciplina': queryset.disciplina,
            }
        else:
            return {
                'aluno': 'Anonimo',
                'professor': 'Anonimo',
                'instituto': 'Escola Secundária Geral de Quelimane',
                'cidade': 'Quelimane',
                'disciplina': 'Quimica',
            }
    @sync_to_async
    def get_context(self, code):
        datas = []
        query_set = Thesis.objects.filter(code=code)
        if query_set:
            for data in query_set:
                datas.append(data.title)
                datas.append(data.text)
        return datas
    
    @sync_to_async
    def save_thesis_content(self, user, tema, titulo, conteudo, institute, disciplina, student, instructor, cidade, code):
        # Salvar conteúdo gerado no banco de dados
        Thesis.objects.create(
            author=user,
            topic=tema,
            title=titulo,
            text=conteudo,
            institute=institute,
            disciplina=disciplina,
            student=student,
            instructor=instructor,
            cidade=cidade,
            code=code
        )
        logger.info('Content saved: %s for user %s', titulo, user)