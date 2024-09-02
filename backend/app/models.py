from django.db import models
from django.contrib.auth.models import User

class Thesis(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(null=True, blank=True, max_length=100)
    disciplina = models.CharField(null=True, blank=True, max_length=100)
    student = models.CharField(null=True, blank=True, max_length=100)
    instructor = models.CharField(null=True, blank=True, max_length=100)
    cidade = models.CharField(null=True, blank=True, max_length=100)
    code = models.CharField(null=True, blank=True, max_length=50)
    topic = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.TextField()
    html = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'({self.topic}) {self.title}' 
