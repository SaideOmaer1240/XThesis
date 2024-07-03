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
from .models import Thesis

logger = logging.getLogger(__name__)

class Esboco:
    def indice(self):
        return ["Introdução", "Objetivo Geral", "Objetivos Específicos", "metodologia",]
  

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

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.error('Invalid JSON received: %s', e)
            await self.send(text_data=json.dumps({'error': 'Dados JSON inválidos'}))
            return

        tema = data.get('tema', 'tema padrão')
        user_id = data.get('user_id')
        institute = data.get('institute')
        disciplina = data.get('disciplina')
        student = data.get('student')
        instructor = data.get('instructor')
        cidade = data.get('cidade')

        if not all([tema, user_id, institute, disciplina, student, instructor, cidade]):
            logger.error('Missing required fields in received data')
            await self.send(text_data=json.dumps({'error': 'Campos obrigatórios faltando'}))
            return

        try:
            user = await sync_to_async(User.objects.get)(id=user_id)
            logger.info('User found: %s', user)
        except User.DoesNotExist:
            logger.error('User not found')
            await self.send(text_data=json.dumps({'error': 'Usuário não encontrado'}))
            return

        groq_api_key = settings.GROQ_API_KEY
        llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")

        prompts = {
            "Introdução": """Você é um assistente criador de tese. Sua tarefa é redigir uma introdução  para uma tese seguindo o formato da APA 7ª edição. 
                A introdução deve ser escrita de forma acadêmica e formal. Inclua citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]."
                Sua tarefa inicial é desenvolver estritamente apenas a introdução. Está proibido desenvolver outras seções sem que eu mencione.
                Veja o exemplo a seguir de uma introdução sobre conjuntivite:

                <h2>Introdução</h2>
                <div>
                <p>A conjuntivite é uma inflamação da conjuntiva, a membrana mucosa que reveste a parte interna das pálpebras e a superfície anterior do globo ocular. Esta condição oftalmológica pode ser classificada em diferentes tipos, sendo os mais comuns a conjuntivite alérgica, aguda e bacteriana. Cada uma dessas formas de conjuntivite possui etiologias distintas, quadros clínicos variados e requer abordagens diagnósticas e terapêuticas específicas.</p>

                <p>Segundo Smith (2020), a conjuntivite alérgica é uma resposta imunológica a alérgenos ambientais como pólen, ácaros e pelos de animais. Esta forma de conjuntivite é frequentemente sazonal, ocorrendo em períodos específicos do ano em que há maior exposição aos alérgenos. Clinicamente, os pacientes apresentam prurido ocular intenso, lacrimejamento, hiperemia conjuntival e edema palpebral.</p>

                <p>A conjuntivite aguda, por outro lado, geralmente resulta de infecções virais ou bacterianas. Segundo Johnson (2018), a conjuntivite viral é frequentemente associada a adenovírus, sendo altamente contagiosa e caracterizada por hiperemia conjuntival, secreção serosa e linfadenopatia pré-auricular. A conjuntivite bacteriana, conforme descreve Brown (2017), é causada por patógenos como Staphylococcus aureus e Streptococcus pneumoniae, e apresenta secreção purulenta, dor ocular moderada e aderência das pálpebras ao despertar.</p>

                <p>Os meios auxiliares de diagnóstico são fundamentais para diferenciar as diversas formas de conjuntivite. Segundo Thompson (2019), a citologia de raspado conjuntival e a cultura bacteriana são métodos importantes para a identificação do agente etiológico, especialmente nas conjuntivites bacterianas e virais. O diagnóstico diferencial é igualmente crucial, pois outras condições oculares, como uveítes e ceratites, podem apresentar sintomas semelhantes.</p>

                <p>A conduta terapêutica varia de acordo com o tipo de conjuntivite. No caso da conjuntivite alérgica, o uso de anti-histamínicos e estabilizadores de mastócitos é frequentemente recomendado. Para a conjuntivite bacteriana, o tratamento com antibióticos tópicos é essencial para a resolução da infecção. Além disso, medidas preventivas, como a higiene adequada das mãos e a evitar o compartilhamento de toalhas e lenços, são importantes para reduzir a transmissão das conjuntivites infecciosas.</p>

                <p>Este estudo visa proporcionar uma compreensão aprofundada sobre os diferentes tipos de conjuntivite, explorando suas características clínicas, métodos diagnósticos e abordagens terapêuticas, com o intuito de aprimorar a prática clínica e melhorar os resultados para os pacientes afetados por esta condição oftalmológica.</p> <div>

                ---

                Tenha em mente que a introdução apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a introdução para este título:  {question} """,
            
            "Objetivo Geral": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Objetivo Geral para uma tese seguindo o formato da APA 7ª edição. 
            O Objetivo Geral deve ser escrito de forma acadêmica e formal. 
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Objetivo Geral. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de um Objetivo Geral:

            <h2>Objetivo Geral<h2>
            <div>
            <p>O objetivo geral deste trabalho é investigar e caracterizar os diferentes tipos de conjuntivite, com ênfase nas formas alérgica, aguda e bacteriana, analisando suas etiologias, quadros clínicos, métodos diagnósticos, condutas terapêuticas e estratégias de prevenção, a fim de fornecer uma base sólida de conhecimento que contribua para a prática clínica e para a melhoria dos resultados no tratamento dos pacientes.</p><div>

            ---

            Tenha em mente que o Objetivo Geral apresentado anteriormente é apenas um modelo para você seguir. Agora, desenvolva o Objetivo Geral para este título: {question}""",
            
            "Objetivos Específicos": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Objetivos Específicos para uma tese seguindo o formato da APA 7ª edição. 
            Os Objetivos Específicos devem ser escritos de forma acadêmica e formal. 
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Objetivos Específicos. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de Objetivos Específicos:

            <h2>Objetivos Específicos</h2>
            <div>
            <ul>
            <li>Conceituar e diferenciar os tipos de conjuntivite.</li>
            <li>Investigar a etiologia de cada tipo de conjuntivite.</li>
            <li>Descrever o quadro clínico de cada tipo de conjuntivite.</li>
            <li>Avaliar os meios auxiliares de diagnóstico.</li>
            <li>Realizar o diagnóstico diferencial.</li>
            <li>Propor condutas terapêuticas específicas.</li>
            <li>Sugerir estratégias de prevenção.</li>
            </ul>
            </div>
            ---

            Tenha em mente que os Objetivos Específicos apresentados anteriormente são apenas um modelo para você seguir. Agora, desenvolva os Objetivos Específicos para este título: {question} """,
            "metodologia": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Metodologia para uma tese seguindo o formato da APA 7ª edição. 
            A Metodologia deve ser escrita de forma acadêmica e formal. Inclua citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]."
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Metodologia. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de uma Metodologia:

            <h2>Metodologia</h2>
            <div>
            <p>O presente trabalho utilizou a metodologia de revisão literária. A revisão literária é uma abordagem metodológica que envolve a busca, análise e síntese de estudos e publicações existentes sobre um determinado tema. Este tipo de metodologia é frequentemente utilizado para compreender o estado da arte de um tópico específico, identificar lacunas na literatura, e consolidar conhecimentos dispersos em uma única fonte.</p>

            <p>Segundo Silva (2015), a revisão literária permite uma visão abrangente e crítica das pesquisas já realizadas, oferecendo uma base sólida para futuras investigações. Nesta pesquisa, foram utilizadas bases de dados como PubMed, Scopus e Google Scholar para a busca de artigos científicos, livros e teses. Os critérios de inclusão abrangeram publicações dos últimos dez anos, escritas em inglês, português e espanhol, e que abordassem diretamente o tema em questão.</p>
            
            <p>O processo de seleção dos estudos incluiu a leitura dos títulos e resumos, seguida pela análise completa dos textos que atendiam aos critérios de inclusão. As informações relevantes foram extraídas e categorizadas em temas principais para facilitar a síntese e a discussão dos achados.</p>

            <p>Além da revisão literária, foi realizada uma análise qualitativa dos dados coletados, conforme sugerido por Minayo (2012), para identificar padrões e tendências na literatura revisada. Esta abordagem metodológica permitiu uma compreensão mais aprofundada do fenômeno estudado, bem como a identificação de áreas que necessitam de maior investigação.</p>
            </div>
            ---

            Tenha em mente que a Metodologia apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a Metodologia para este título: {question}  """,
            
            "desenvolvimento": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção desenvolvendo um tema específico para uma tese seguindo o formato da APA 7ª edição. A seção deve ser escrita de forma acadêmica e formal, e deve incluir citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]." 
            Sua tarefa inicial é desenvolver estritamente apenas a seção mencionada. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de uma seção sobre Diagnóstico Diferencial:

            <h2>Diagnóstico Diferencial</h2>
            <div>
            <p>O diagnóstico diferencial da conjuntivite é um passo crucial para assegurar que o tratamento apropriado seja administrado e para evitar complicações decorrentes de diagnósticos incorretos. Dada a variedade de condições oftalmológicas que podem apresentar sintomas semelhantes aos da conjuntivite, é essencial distinguir entre elas com precisão. Segundo Johnson (2019), uma avaliação detalhada do histórico médico do paciente, um exame físico cuidadoso e, quando necessário, exames laboratoriais adicionais são fundamentais para esse processo.</p>

            <p><strong>Conjuntivite Alérgica vs. Outras Alergias Oculares:</strong> A conjuntivite alérgica deve ser diferenciada de outras formas de alergia ocular, como a queratoconjuntivite atópica e a conjuntivite vernal. Ambas podem apresentar sintomas como prurido, lacrimejamento e hiperemia conjuntival, mas tendem a ser mais graves e crônicas. Segundo Miller (2018), a presença de papilas gigantes na conjuntiva tarsal é um indicativo de conjuntivite vernal, enquanto a queratoconjuntivite atópica pode envolver alterações na pele ao redor dos olhos.</p>

            <p><strong>Conjuntivite Viral vs. Conjuntivite Bacteriana:</strong> Diferenciar entre conjuntivite viral e bacteriana é essencial, pois as abordagens terapêuticas são distintas. Segundo Roberts (2020), a conjuntivite viral geralmente apresenta secreção aquosa e sintomas sistêmicos como febre e linfadenopatia pré-auricular, enquanto a conjuntivite bacteriana se caracteriza por secreção purulenta espessa e adesão das pálpebras ao acordar. A história de exposição recente a uma pessoa infectada pode ajudar a sugerir uma etiologia viral.</p>
            </div>

            ---

            Tenha em mente que a seção apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a seção para este titulo: {question}""",
            "Referências": """Crie a referência bibliográfica seguindo esse conteúdo context: {question}""",
            "Conclusão": """"Você é um assistente criador de tese. Sua tarefa é redigir uma conclusão para uma tese seguindo o formato da APA 7ª edição. A conclusão deve ser escrita de forma acadêmica e formal, e deve incluir citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]."
        Sua tarefa inicial é desenvolver estritamente apenas a conclusão. Está proibido desenvolver outras seções sem que eu mencione.
        Veja o exemplo a seguir de uma conclusão sobre conjuntivite:

        <h2>Conclusão</h2>
        <p>A conjuntivite, em suas diferentes formas – alérgica, aguda e bacteriana – é uma condição oftalmológica comum que afeta uma ampla faixa da população. Através deste trabalho, foi possível explorar de maneira detalhada os conceitos, a etiologia, o quadro clínico, os meios auxiliares de diagnóstico, o diagnóstico diferencial, as condutas terapêuticas e as estratégias de prevenção relacionados a cada tipo de conjuntivite.

        A compreensão das características específicas de cada tipo de conjuntivite é essencial para um diagnóstico preciso e um tratamento eficaz. Segundo Johnson (2019), a distinção entre conjuntivite viral, bacteriana e alérgica, por meio de uma avaliação clínica cuidadosa e, quando necessário, exames laboratoriais, permite a implementação de estratégias terapêuticas direcionadas que melhoram os resultados para os pacientes.

        As medidas preventivas, incluindo práticas de higiene pessoal, controle de alérgenos, uso adequado de lentes de contato, vacinação e campanhas de conscientização, desempenham um papel crucial na redução da incidência e na propagação da conjuntivite. Segundo Thompson (2020), a educação contínua e a adoção de políticas preventivas em ambientes coletivos são fundamentais para controlar surtos e proteger a saúde ocular da comunidade.

        Esta pesquisa contribui para o entendimento aprofundado da conjuntivite e fornece uma base sólida de conhecimento que pode ser utilizada por profissionais de saúde na prática clínica diária. A identificação das lacunas no conhecimento atual e a sugestão de áreas para futuras pesquisas também são aspectos importantes desta tese, incentivando o contínuo avanço no diagnóstico, tratamento e prevenção da conjuntivite.</p>

        ---

        Tenha em mente que a conclusão apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a conclusão para este tema:{question}
                    
                    """,
        "Referências": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de bibliografia seguindo o formato da APA 7ª edição. 
A bibliografia deve ser escrita de forma acadêmica e formal, listando todas as referências usadas na tese. 
Sua tarefa inicial é desenvolver estritamente apenas a seção de bibliografia. Está proibido desenvolver outras seções sem que eu mencione.
Veja o exemplo a seguir de uma bibliografia:

<h2>References</h2>
<p>Bickford, D., Lavery, T. J., & Hero, J.-M. (2012). Conserving amphibians: A review of the role of environmental factors. <i>Mammal Review, 42</i>(2), 135-151.</p>

<p>Hero, J.-M., & Todd, B. D. (2014). Amphibian ecology and conservation. <i>Journal of Experimental Biology, 217</i>(2), 249-258.</p>

<p>Mace, G. M., et al. (2018). Quantifying the impacts of habitat fragmentation on amphibian populations. <i>Conservation Biology, 32</i>(4), 759-769.</p>

<p>Ransom, K. L., et al. (2020). Climate change and amphibian ecology: A review of the current evidence. <i>Journal of Experimental Biology, 223</i>(11), jeb204615.</p>

---

Tenha em mente que a bibliografia apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a bibliografia para as seguinte tema:{question}

        
        """
        }

        prompt_template = """Você é um assistente criador de indice de tese. Sua tarefa é redigir um índice para uma tese, o indice deve estar em uma lista python. 
        O índice deve ser escrito de forma acadêmica e formal, utilizando tópicos hierarquicamente organizados. Está proibido desenvolver outras seções sem que eu mencione.
        Veja o exemplo a seguir de um índice:

        topicos = [
            "Introdução", 
            "Objetivo Geral",
            "Objetivos Específicos",
            "A diarreia crônica Estádio IV",
            "A diarreia crônica no estádio IV nos pacientes com HIV",
            "O tratamento da diarreia crônica",
            "Critérios de diagnósticos",
            "Síndrome de caquexia",
            "Tratamento da Síndrome de Caquexia com Eritromicina",
            "Evidências Clínicas",
            "Estudos e Resultados",
            "Índice de Massa Corporal (IMC)",
            "Conclusão",
            "Referências"
        ]

        ---

        Tenha em mente que o índice apresentado anteriormente é apenas um modelo para você seguir. Agora, desenvolva o índice para este título: {question}.
                """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        outline_chain = (
            prompt
            | llm
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
         

        for elemento in sumario:
            if elemento not in indice:
                indice.append(elemento)
         

        total_items = len(indice)
        processed_items = 0

        for titulo in indice:
            logger.info('Processing title: %s', titulo)
            if titulo.lower() in prompts:
                prompt_text = prompts[titulo.lower()] + tema
            else:
                prompt_text = prompts["desenvolvimento"]

            linha_de_saida = ChatPromptTemplate.from_template(prompt_text)
            chain = (
                linha_de_saida
                | llm
                | StrOutputParser()
            )

            try:
                pretextual = ["Introdução", "Objetivo Geral", "Objetivos Específicos", "metodologia",]
                if titulo.lower() == "bibliografia":
                    response = await sync_to_async(chain.invoke)({"context": "conteúdo de exemplo"})
                 
                elif titulo.lower() == 'introdução':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                elif titulo.lower() == 'objetivo geral':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                elif titulo.lower() == 'objetivos específicos':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                elif titulo.lower() == 'metodologia':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                elif titulo.lower() == 'conclusão':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                elif titulo.lower() == 'referências':
                    response = await sync_to_async(chain.invoke)({"question": tema})
                else:
                    for texto in pretextual:
                        if titulo.lower() != texto.lower():
                            response = await sync_to_async(chain.invoke)({"question": titulo})
                        elif titulo.lower() == texto.lower():
                            response = await sync_to_async(chain.invoke)({"question": tema})

                logger.info('Processo concluido com sucesso da tarefa %s: %s', titulo)
                
                regex = r'<div\b[^>]*>(.*?)<\/div>'
                resultados = re.findall(regex, response, re.DOTALL)
                results = ' '.join(resultados)

                # Salvar no banco de dados
                await self.save_thesis_content(user, tema, titulo, results, institute, disciplina, student, instructor, cidade)

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

            await asyncio.sleep(5)  # Ajustado para reduzir o tempo de espera

    async def disconnect(self, close_code):
        logger.info('WebSocket connection closed with code %s', close_code)

    @sync_to_async
    def save_thesis_content(self, user, tema, titulo, conteudo, institute, disciplina, student, instructor, cidade):
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
            cidade=cidade
        )
        logger.info('Content saved: %s for user %s', titulo, user)
