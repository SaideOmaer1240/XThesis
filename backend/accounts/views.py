from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from app.permissions import IsAuthor
from app.models import Thesis
from . datetime import DateTime
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
   
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Adicione mais campos conforme necessário
        }
        return Response(user_data)
    

class CredentialsView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]   
     
    def get(self, request):
        user = request.user
        topic_name = request.query_params.get('topic_name')
        queryset = Thesis.objects.filter(author=user)
        
        mes = DateTime.get_month()
        ano = DateTime.year()
        if topic_name: 
            queryset = queryset.filter(topic=topic_name)
            first_thesis = queryset.filter(topic=topic_name).first()
            if first_thesis:
                credentials = {
                'city': first_thesis.cidade,
                'disciplina': first_thesis.disciplina,
                'institute' :first_thesis.institute,
                'instructor' :first_thesis.instructor,
                'student' :first_thesis.student,
                'topic' : first_thesis.topic,
                'month': mes,
                'year' : ano,
                }         
        return Response(credentials)
    
