import google.generativeai as genai 
import os
class GoogleAIChat: 
    def __init__(self, api_key=None, temperature=1, top_p=0.95, top_k=64, max_output_tokens=8192, response_mime_type="text/plain"):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or an environment variable 'GEMINI_API_KEY'.")

        genai.configure(api_key=self.api_key)
        
        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": response_mime_type,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
            # safety_settings can be adjusted if needed
        )

        self.chat_session = self.model.start_chat(history=[])

    def send_message(self, message):
        response = self.chat_session.send_message(message)
        return response.text







