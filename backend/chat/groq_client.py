from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
 
class GroqChatClient:
    def __init__(self, model_name="llama3-70b-8192", temperature=0):
        self.api_key = settings.GROQ_API_KEY
        self.llm = ChatGroq(temperature=temperature, groq_api_key=self.api_key, model_name=model_name)
        self.prompt_template = """Memória recorrente: {memoria} \n\nVocê é um assistente de IA. Por favor, responda com base no seu conhecimento: {question}"""
        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)
        self.outline_chain = self.prompt | self.llm | StrOutputParser()

    def get_response(self, question: str, memoria: str) -> str:
        try:
            response = self.outline_chain.invoke({"memoria": memoria, "question": question})
            return response
        except Exception as e:
            # Log error or handle it accordingly
            print(f"Error getting response: {e}")
            return "Erro ao processar a solicitação."

# Exemplo de uso:
# groq_client = GroqChatClient()
# response = groq_client.get_response('o que é llm')
# print(response)
