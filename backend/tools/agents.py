from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings 
from .prompt import ThesisIndexPrompt, ThesisDevelopmentPrompt
import google.generativeai as genai
import re   
from groq import Groq
import os
from langchain_google_genai import ChatGoogleGenerativeAI 
import PIL.Image
from django.core.files.storage import default_storage
import os 

class AudioTranscriber:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def get_response(self, file, user):
        # Pegue o nome do usuário
        username = str(user) # Converta o objeto User para o nome do usuário

        # Crie o subdiretório com o nome do usuário se não existir
        directory = os.path.join(settings.MEDIA_ROOT, 'recordings', username)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Verifique se o arquivo tem o método temporary_file_path
        if hasattr(file, 'temporary_file_path'):
            file_path = file.temporary_file_path()
        else:
            # Caso contrário, salve o arquivo no sistema de arquivos
            file_name = file.name
            file_path = default_storage.save(os.path.join(directory, file_name), file)
            file_path = default_storage.path(file_path)

        # Abra o arquivo e faça a transcrição
        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=(file.name, audio_file.read()),
                model="whisper-large-v3",
                prompt="Specify context or spelling",
                response_format="json",
                language="pt",
                temperature=0.0
            )

        # Limpe o arquivo temporário se necessário
        if not hasattr(file, 'temporary_file_path'):
            os.remove(file_path)

        # Elimine todos os arquivos com extensão .webm no diretório
        for filename in os.listdir(directory):
            if filename.endswith(".webm"):
                os.remove(os.path.join(directory, filename))

        return transcription.text


 
class Multimodal:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY 
        genai.configure(api_key=self.api_key)
        self.llm = genai.GenerativeModel(model_name="gemini-1.5-flash")
          
    
    def get_response(self, image_message):
        img = PIL.Image.open(image_message)
        system_msg = "Analise a imagem fornecida e descreva-a com o máximo de detalhes possível. Caso existam letras ou textos na imagem, transcreva-os integralmente. Garanta que todas as informações visuais relevantes sejam mencionadas, incluindo cores, formas, objetos, contextos e quaisquer outros elementos presentes. Se for codigo depois da descrição, escreva o codigo da respetiva linguaguem presente na imagem, se for problema matematico, depois da descrição resolva o problema e apresente a resposta."
        response = self.llm.generate_content([system_msg, img])
        return response.text
    

    
index_prompt = ThesisIndexPrompt()
prompt_title = ThesisDevelopmentPrompt()
class Escritor:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL_NAME
        self.llm = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model_name)
        #self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",temperature=0, max_tokens=None,timeout=None,max_retries=2, google_api_key=settings.GEMINI_API_KEY)
        self.parser = StrOutputParser()
        print("processado") 
         
    
    def generate_index(self, topic : str, lang : str) -> list:
        
        system_msg = index_prompt.get_prompt(lang)
        human_msg = index_prompt.get_instrutor(lang)
        prompt = ChatPromptTemplate.from_messages(
            
            
            [
                ("system", system_msg),
                            
                 
                ("human", human_msg + '"{topic}"')
            ]
        )
        print("processado: MessagesPlaceholder d")
        chain = prompt | self.llm | self.parser
        
        try:
            response = chain.invoke(
                {"topic": topic}
            )
            text = str(response)
            matches = re.findall(r'\[(.*?)\]', text, re.DOTALL)
            content = str(matches[0])
            match  = re.findall(r'"(.*?)"', content)
            indice = [item for item in match if not (item.startswith("1.1") or any(item.startswith(f"1.{i}") for i in range(2, 10)))]
            return indice
        except Exception as e:
           print(f"Erro ao tentar obter o índice para o trabalho: {topic}\n Tipo de erro: {e}")
           lista_vasia = []
           return lista_vasia
       
    def generate_response(self, title : str, index : list, lang : str) -> str:
        system_msg = prompt_title.get_prompt(lang)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system"
                    , system_msg  
                ) , 
                ("human", 'Este é o meu esboço:{index}. ignore todas outras sessões e consentre-se em Desenvolver extritamente essa parte: "{title}". texto deve ser escrita na lingua {lang}') 
            ]
        )
        chain = prompt_template | self.llm | self.parser
        try:
            response = chain.invoke({"title":title, "index":index, "lang":lang})
            print(response)
            import time
            time.sleep(7)
            return response
        except Exception as e:
            print(f"Erro ao tentar gerar a resposta para o trabalho: {title}\nTipo de erro: {e}")
            return "Erro ao processar a solicitação."

 

class Translator:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL_NAME
        self.system_msg = """ Atue como um tradutor profissional especializado em múltiplos idiomas. Você tem       
                Sua tarefa é traduzir o seguinte texto para o idioma solicitado. Ao fornecer a tradução, retorne o resultado em um formato JSON, conforme o exemplo abaixo. Certifique-se de que a tradução seja clara, precisa e que respeite as nuances do idioma de destino.
                **Formato de saída esperado:**
                ```json
                  "traduzido": "Tradução aqui" ```
                **Instruções:**
                1. Receba o texto a ser traduzido e identifique o idioma de destino.
                2. Realize a tradução com foco na precisão e na preservação do significado original.
                3. Retorne a tradução no formato JSON conforme especificado.
                **Exemplo de uso:**
                Texto de entrada: "Você fala bem de mim."
                Idioma de destino: Inglês
                **Saída esperada:**
                  ```json
                  "traduzido": "You speak well of me" 
                ```
                **Importante:** Mantenha a estrutura JSON limpa e sem erros de sintaxe.

        
                   """
        self.llm = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model_name)
        self.parser = StrOutputParser()
        print("processado")
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", self.system_msg
                ),  
                
                ("human", 'Texto de entrada:{text}. Idioma de destino: {lang}') 
            ]
        ) 
        self.chain = self.prompt_template | self.llm | self.parser 
    
    def translate(self, text: str, lang: str) -> str:
        # Solicita ao modelo que traduza o texto
         response = self.chain.invoke({"text":text, "lang":lang})
         resultado = re.search(r'\"traduzido\": \"(.*?)\"', response)
         texto_localizado = resultado.group(1)
         return texto_localizado 
     
  
class TitleGenerator:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL_NAME
        self.system_msg = """Atue como um gerador de títulos para conversas entre um usuário e um modelo de linguagem (LLM). 
                Sua tarefa é criar um título relevante e conciso que capture a essência da conversa. 
                O título deve ser informativo e refletir o tema ou o objetivo principal da interação.
                
                **Formato de saída esperado:**
                ```json
                  "titulo": "Título gerado aqui" ```
                **Instruções:**
                1. Receba o texto da conversa e analise seu conteúdo.
                2. Gere um título que resuma o objetivo ou tema principal da conversa.
                3. Retorne o título no formato JSON conforme especificado.
                **Exemplo de uso:**
                Texto da conversa: "Usuário pergunta como integrar a API X no sistema Y."
                **Saída esperada:**
                  ```json
                  "titulo": "Integração da API X no Sistema Y" 
                ```
                **Importante:** Mantenha a estrutura JSON limpa e sem erros de sintaxe.
                   """
        self.llm = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model_name)
        self.parser = StrOutputParser()
        print("processado")
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", self.system_msg
                ),  
                
                ("human", 'Texto da conversa: {text}') 
            ]
        ) 
        self.chain = self.prompt_template | self.llm | self.parser 
    
    def generate_title(self, text: str) -> str:
        # Solicita ao modelo que gere o título da conversa
        response = self.chain.invoke({"text":text})
        resultado = re.search(r'\"titulo\": \"(.*?)\"', response)
        titulo_gerado = resultado.group(1)
        return titulo_gerado 
 