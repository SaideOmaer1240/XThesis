from .models import Message
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from django.conf import settings
import os

class ChatService:
    def __init__(self, model_name="llama3-8b-8192"):
        # Configurar a API Key
        self.api_key = settings.GROQ_API_KEY
        self.model = ChatGroq(model=model_name, api_key=self.api_key)
        print(f"ChatService initialized with model: {model_name} and api_key: {self.api_key}")

    def get_session_history(self, session_id):
        print(f"Fetching session history for session_id: {session_id}")
        messages = Message.objects.filter(session_id=session_id).order_by('created_at')
        history = []
        for msg in messages:
            if msg.is_user:
                history.append(HumanMessage(content=msg.text))
            else:
                history.append(HumanMessage(content=msg.text, role="assistant"))
        print(f"Session history: {history}")
        return history

    def create_message(self, session_id, text, is_user):
        print(f"Creating message - Session ID: {session_id}, Text: {text}, Is User: {is_user}")
        return Message.objects.create(
            session_id=session_id,
            text=text,
            is_user=is_user
        )

    def get_response(self, user_input, session_id):
        print(f"get_response called with user_input: {user_input} and session_id: {session_id}")
        
        # Armazenar a mensagem do usuário
        self.create_message(session_id, user_input, is_user=True)

        # Criação e invocação do modelo com histórico
        runnable_with_history = RunnableWithMessageHistory(
            self.model,
            lambda sid: self.get_session_history(sid)  # A função retorna a lista de mensagens diretamente
        )

        history = self.get_session_history(session_id)
        print(f"History for runnable: {history}")
        
        try:
            response = runnable_with_history.invoke(
                [HumanMessage(content=user_input)],
                config={"configurable": {"session_id": session_id}},  # Passa apenas o session_id
            )
            print(f"Model response: {response}")
        except Exception as e:
            print(f"Error invoking model: {e}")
            raise e

        # Armazenar a resposta do modelo
        self.create_message(session_id, response.content, is_user=False)
        return response.content
