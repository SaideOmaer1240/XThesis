from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserData(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    professor = models.CharField(null=True, blank=True, max_length=50)
    aluno = models.CharField(null=True, blank=True, max_length=50)
    instituto = models.CharField(null=True, blank=True, max_length=50)
    cidade = models.CharField(null=True, blank=True, max_length=50)
    disciplina = models.CharField(null=True, blank=True, max_length=50)
    
    
    def __str__(self):
        return f'{self.aluno}'
