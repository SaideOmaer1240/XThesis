 
from django.urls import path
from .views import  UserProfileView, CredentialsView, CheckAvailability

 
urlpatterns = [
    path('user/info/',  UserProfileView.as_view(), name='user-profile'),
    path('author/credentials/',  CredentialsView.as_view(), name='author-credentials'),
     path('check-availability/', CheckAvailability.as_view(), name='check_availability'),
     ]
 
