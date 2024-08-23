from django.urls import path
from .views import ChatbotView, GetMessagesView, GetSessionsView, StartNewSessionView 
urlpatterns = [
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('get_messages/', GetMessagesView.as_view(), name='get_messages'),
    path('get_sessions/', GetSessionsView.as_view(), name='get_sessions'),
    path('start_new_session/', StartNewSessionView.as_view(), name='start_new_session'),
]  

