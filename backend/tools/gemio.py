import os
import google.generativeai as genai

class GeminiAIModel:
    def __init__(self, api_key: str, model_name: str, generation_config: dict):
        self.api_key = api_key
        self.model_name = model_name
        self.generation_config = generation_config
        self._configure_api()
        self.model = self._create_model()
        
    def _configure_api(self):
        genai.configure(api_key=self.api_key)
    
    def _create_model(self):
        return genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
        )

    def start_chat(self, history=None):
        if history is None:
            history = []
        return self.model.start_chat(history=history)
    
    def send_message(self, chat_session, message: str):
        response = chat_session.send_message(message)
        return response.text

