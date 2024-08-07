from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings

 
class GroqChatClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        
        self.llm = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name="llama-3.1-70b-versatile")
        self.parser = StrOutputParser()  
        self.prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'Você é uma IA chamada LeonIA, você responde perguntas com respostas simples e sem brincadeiras.\nSe caso o usuário pedir um código, deve escrever neste formato:\n```linguagem\n código \n```:\nExemplo: ```python\n print("Olá, Mundo!")\n```\n```javascrip \nconsole.log("Olá, Mundo!");\n``` \n',
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)  
        self.chain = self.prompt_template | self.llm | self.parser 

    def get_response(self, question: str, memoria: list) -> str:
        try:
            response = self.chain.invoke({"question": question,"chat_history": memoria})
            return response
        except Exception as e:
            # Log error or handle it accordingly
            print(f"Error getting response: {e}")
            return "Erro ao processar a solicitação."
 