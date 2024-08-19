from django.db import models
from django.contrib.auth.models import User
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    title = models.BooleanField(default=False)
    session_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_title = models.CharField(max_length=255, blank=True, null=True)  # Novo campo para o título da sessão

    def save(self, *args, **kwargs):
        if self.is_user and  self.session_title is None:
            self.session_title = self.text[:50]  # Usar os primeiros 50 caracteres da mensagem do usuário como título
        super().save(*args, **kwargs)

