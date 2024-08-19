from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
from .models import Message
import uuid
import logging
from tools.groq_client import GroqChatClient
from tools.agents import CreateTitle
from django.db.models import Max
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)

groq_client = GroqChatClient()
gen_title = CreateTitle()
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

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            logger.debug(f"Data received: {data}")

            user_message = data.get('message')
            session_id = data.get('session_id') or str(uuid.uuid4())

            if not user_message:
                return Response({'error': 'Mensagem não fornecida'}, status=400)
            
            non_user_messages_exist = Message.objects.filter(session_id=session_id, is_user=False).exists()
            if  non_user_messages_exist:
                all_messages = Message.objects.all().order_by('created_at')
                chat = []
                for i in all_messages:
                    if i.is_user:
                         chat.append(HumanMessage(content=i.text))
                    else:
                         chat.append(AIMessage(content=i.text))
 
            # Verificar se existe algum message com title=False
            title = Message.objects.filter(session_id=session_id, title=False).exists()
 
            if title:  
                titulo = gen_title.get_title(cha) 
                session_title = titulo[:50]
                Message.objects.filter(session_id=session_id).update(session_title=session_title)
                Message.objects.filter(session_id=session_id).update(title=True)

            memoria = []
            previous_messages = Message.objects.filter(session_id=session_id).order_by('created_at')
            for i in previous_messages:
                if i.is_user:
                    memoria.append(HumanMessage(content=i.text))
                else:
                    memoria.append(AIMessage(content=i.text))

            response = groq_client.get_response(question=user_message, memoria=memoria)
            user = request.user
            Message.objects.create(user=user, text=user_message, is_user=True, session_id=session_id)
            response_text = response
            Message.objects.create(text=response_text, is_user=False, session_id=session_id)

            return Response({'response': response_text, 'session_id': session_id})

        except json.JSONDecodeError:
            logger.error("Invalid JSON")
            return Response({'error': 'Dados fornecidos são inválidos'}, status=400)
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
            return Response({'error': str(e)}, status=500)
