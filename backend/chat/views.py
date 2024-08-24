from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser 
import json
import uuid
import logging
from django.db.models import Max
from .models import Message
from tools.groq_client import GroqChatClient 
from langchain_core.messages import HumanMessage, AIMessage
from tools.agents import Multimodal, AudioTranscriber
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from tools.utils import UserName
from django.conf import settings 
import os
logger = logging.getLogger(__name__)

User = UserName()
groq_client = GroqChatClient() 
vision_model = Multimodal()
audio_model = AudioTranscriber()

class StartNewSessionView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            new_session_id = str(uuid.uuid4())
            return Response({'session_id': new_session_id})
        except Exception as e:
            logger.error(f"Error in StartNewSessionView: {e}")
            return Response({'error': 'Erro interno do servidor'}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]   

    def post(self, request, *args, **kwargs):
        try:
            # Extrair a mensagem do usuário
            user_message = request.data.get('message')
            userId = request.data.get('userId')
            session_id = request.data.get('session_id') or str(uuid.uuid4())
            image = request.FILES.get('image')   
            audio = request.FILES.get('audio')
            print(userId)
            
            username = User.get_user_by_id(userId)

            if not user_message:
                return Response({'error': 'Mensagem não fornecida, ou qualquer arquivo para ser processado.'}, status=400)

            # Processamento da mensagem e da imagem
            memoria = []
            previous_messages = Message.objects.filter(session_id=session_id).order_by('created_at')
            for msg in previous_messages:
                if msg.is_user:
                    memoria.append(HumanMessage(content=msg.text))
                else:
                    memoria.append(AIMessage(content=msg.text))

            titulo_recente = Message.get_session_title(session_id)
            if titulo_recente:
                title = titulo_recente
            else:
                title = 'Nova conversa'

            Message.destroy_old_message(session_id) 
            
            if image:
                logger.debug(f"Imagem recebida: {image.name}") 

                # Crie o subdiretório com o nome do usuário se não existir
                directory = os.path.join(settings.MEDIA_ROOT, 'recordings', str(username))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                # Crie o caminho completo para o arquivo
                file_path = os.path.join(directory, image.name)

                # Salvar a imagem no servidor
                path = default_storage.save(file_path, ContentFile(image.read()))
                image_full_path = default_storage.path(path)
                logger.debug(f"Imagem salva em: {image_full_path}")

                # Usar o modelo de visão para processar a imagem
                response = vision_model.get_response(image_message=image_full_path)

                # Remover todos os arquivos no diretório após o processamento
                for filename in os.listdir(directory): 
                    os.remove(os.path.join(directory, filename))

            else:
            # Obtenha a resposta do chatbot
                if audio:
                    print(username)
                    user_message = audio_model.get_response(audio, user=username)
                response = groq_client.get_response(question=user_message, memoria=memoria)
            user = request.user
            Message.objects.create(user=user, text=user_message, is_user=True, session_id=session_id, session_title=title)
            Message.objects.create(text=response, is_user=False, session_id=session_id, session_title=title)

            return Response({'response': response, 'session_id': session_id})

        except Exception as e:
            logger.error(f"Error in ChatbotView: {e}")
            return Response({'error': 'Erro interno do servidor'}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class GetMessagesView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            
            if not session_id:
                return Response({'error': 'ID da sessão não fornecido'}, status=400)

            messages = Message.objects.filter(session_id=session_id).order_by('created_at')
            messages_data = [{'text': msg.text, 'is_user': msg.is_user} for msg in messages]

            return Response({'messages': messages_data})
        except json.JSONDecodeError:
            logger.error("Invalid JSON")
            return Response({'error': 'Dados fornecidos são inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error in GetMessagesView: {e}")
            return Response({'error': 'Erro interno do servidor'}, status=500)

class GetSessionsView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            latest_messages = (
                Message.objects
                .filter(is_user=True, user=user)
                .values('session_id')
                .annotate(latest_message_id=Max('id'))
                .values_list('latest_message_id', flat=True)
            )
            
            latest_message_details = Message.objects.filter(id__in=latest_messages)
            
            sessions = [
                {
                    'session_id': str(message.session_id),
                    'session_title': message.session_title,
                    'text': message.text,
                    'created_at': message.created_at.isoformat()
                }
                for message in latest_message_details
            ]
            
            return Response({'sessions': sessions}, status=200)
        except Exception as e:
            logger.error(f"Error in GetSessionsView: {e}")
            return Response({'error': 'Erro interno do servidor'}, status=500)

