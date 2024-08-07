from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .transcriber import AudioTranscriber

class TranscribeAudioView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    transcriber = AudioTranscriber()

    def post(self, request, *args, **kwargs):
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio file provided'}, status=400)

        file = request.FILES['audio']
        try:
            transcription_text = self.transcriber.transcribe(file)
            return Response({"text": transcription_text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
