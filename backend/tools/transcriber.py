import os
from groq import Groq

class AudioTranscriber:
    def __init__(self):
        self.client = Groq()

    def transcribe(self, file):
        with open(file.temporary_file_path(), "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=(file.name, audio_file.read()),
                model="whisper-large-v3",
                prompt="Specify context or spelling",
                response_format="json",
                language="pt",
                temperature=0.0
            )
        return transcription['text']
