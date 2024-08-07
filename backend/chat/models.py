from django.db import models

class Message(models.Model):
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    session_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_title = models.CharField(max_length=255, blank=True, null=True)  # Novo campo para o título da sessão

    def save(self, *args, **kwargs):
        if self.is_user and not self.session_title:
            self.session_title = self.text[:50]  # Usar os primeiros 50 caracteres da mensagem do usuário como título
        super().save(*args, **kwargs)

