from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.conf import settings
from .models import Message 
import uuid
import logging
from .groq_client import GroqChatClient  
from django.db.models import Max

logger = logging.getLogger(__name__)
 
api_key = settings.GROQ_API_KEY
groq_client = GroqChatClient() 

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.conf import settings
from .models import Message 
import uuid
import logging
from .groq_client import GroqChatClient  
from django.db.models import Max

logger = logging.getLogger(__name__)
 
# Configure a chave de API do GROQ
api_key = settings.GROQ_API_KEY
groq_client = GroqChatClient() 
 
@csrf_exempt
def start_new_session(request):
    if request.method == 'POST':
        try:
            # Gera um novo UUID para a sessão
            new_session_id = str(uuid.uuid4())
            return JsonResponse({'session_id': new_session_id})
        except Exception as e:
            logger.error(f"Error in start_new_session view: {e}")
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"Data received: {data}")

            user_message = data.get('message')
            session_id = data.get('session_id') or str(uuid.uuid4())  # Define um novo UUID se não fornecido

            if not user_message:
                return JsonResponse({'error': 'Mensagem não fornecida'}, status=400)

           

            # Atualiza o título da sessão se ainda não estiver definido
            session_title = Message.objects.filter(session_id=session_id).values_list('session_title', flat=True).first()
            if not session_title:
                session_title = user_message[:50]
                Message.objects.filter(session_id=session_id).update(session_title=session_title)

            # Buscar mensagens anteriores na mesma sessão para manter o contexto
            memoria = []
            previous_messages = Message.objects.filter(session_id=session_id).order_by('created_at')
            for i in previous_messages: 
                 if i.is_user == True:
                     user = i.text
                     memoria.append(
                     {
                         'user': user,
                     })
                 else:
                    assistente = i.text
                    memoria.append(
                    { 
                         'assistente': assistente
                     } 
                 )
                 
            memory = str(memoria)

            # Enviar a mensagem do usuário para o modelo GROQ
           
            response = groq_client.get_response(memory, user_message)
            
             # Salvar a mensagem do usuário
            Message.objects.create(text=user_message, is_user=True, session_id=session_id)

            # Acessar o texto da resposta corretamente
            response_text = response 

            # Salvar a resposta do chatbot
            Message.objects.create(text=response_text, is_user=False, session_id=session_id)

            return JsonResponse({'response': response_text, 'session_id': session_id})

        except json.JSONDecodeError:
            logger.error("Invalid JSON")
            return JsonResponse({'error': 'Dados fornecidos são inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error in chatbot view: {e}")
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)

@csrf_exempt
def get_messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')

        messages = Message.objects.filter(session_id=session_id).order_by('created_at')
        messages_data = [{'text': msg.text, 'is_user': msg.is_user} for msg in messages]

        return JsonResponse({'messages': messages_data})

@csrf_exempt
def get_sessions(request):
    if request.method == 'GET':
        try:
            # Obter a última mensagem de cada sessão
            latest_messages = (
                Message.objects
                .filter(is_user=True)
                .values('session_id')
                .annotate(latest_message_id=Max('id'))
                .values_list('latest_message_id', flat=True)
            )
            
            # Obter os detalhes das últimas mensagens
            latest_message_details = Message.objects.filter(id__in=latest_messages)
            
            # Preparar a resposta
            sessions = [
                {
                    'session_id': str(message.session_id),
                    'session_title': message.session_title,
                    'text': message.text,
                    'created_at': message.created_at.isoformat()
                }
                for message in latest_message_details
            ]
            
            return JsonResponse({'sessions': sessions}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)