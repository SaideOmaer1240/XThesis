 
from django.urls import path
from .views import  UserProfileView, CredentialsView

 
urlpatterns = [
    path('user/info/',  UserProfileView.as_view(), name='user-profile'),
    path('author/credentials/',  CredentialsView.as_view(), name='author-credentials'),
     ]
 
