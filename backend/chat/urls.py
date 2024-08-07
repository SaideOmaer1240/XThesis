from django.urls import path
from .views import chatbot, get_messages, get_sessions, start_new_session

urlpatterns = [
    path('chatbot/', chatbot, name='chatbot'),
    path('get_messages/', get_messages, name='get_messages'),
    path('get_sessions/', get_sessions, name='get_sessions'),
    path('start_new_session/', start_new_session, name='start_new_session'),
    
]
