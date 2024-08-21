from django.db import models
from django.contrib.auth.models import User
import uuid
from tools.agents import TitleGenerator

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    title = models.BooleanField(default=False)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    session_title = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Salva a mensagem normalmente
        super().save(*args, **kwargs)

        if not Message.objects.filter(session_id=self.session_id, title=True).exists():
            gen_title = TitleGenerator()
            mensagens = Message.objects.filter(session_id=self.session_id).values_list('text', flat=True)
            texto_completo = " ".join(mensagens)

            titulo = gen_title.generate_title(texto_completo)
            session_title = titulo

            Message.objects.filter(session_id=self.session_id).update(session_title=session_title, title=True)

    @classmethod
    def get_session_title(cls, session_id):
        try:
            # Recupera a mensagem mais antiga com um session_title definido para a session_id fornecida
            message = cls.objects.filter(session_id=session_id, session_title__isnull=False).earliest('created_at')
            return message.session_title
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def destroy_old_message(cls, session_id): 
        non_user_message_count = cls.objects.filter(session_id=session_id, is_user=False).count() 
        user_message_count = cls.objects.filter(session_id=session_id, is_user=True).count() 
        if non_user_message_count >= 10: 
            oldest_non_user_messages = cls.objects.filter(session_id=session_id, is_user=False).order_by('created_at')[:4]
            # Excluir as 4 mensagens mais antigas
            oldest_non_user_messages.delete()
            
        elif user_message_count >= 25:
            user_messages = cls.objects.filter(session_id=session_id, is_user=True).order_by('created_at')[:4]
            # Excluir as 4 mensagens mais antigas
            user_messages.delete()

        