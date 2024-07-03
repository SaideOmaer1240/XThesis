 
from django.urls import path
from .views import  UserProfileView

 
urlpatterns = [
    path('user/info/',  UserProfileView.as_view(), name='user-profile'),
     ]
 
