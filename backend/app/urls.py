
# In urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from django.urls import path
from ..app.views import TopicViewSet, ThesisViewSet, UserProfileView

router = DefaultRouter()

router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'theses', ThesisViewSet, basename='thesis')
 
urlpatterns = [
    path('', include(router.urls)), 
    path('user/info/',  UserProfileView.as_view(), name='user-profile'),
     ]
 
