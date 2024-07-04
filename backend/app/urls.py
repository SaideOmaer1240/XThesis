
# In urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from django.urls import path
from .views import TopicViewSet, ThesisViewSet 
router = DefaultRouter()

router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'theses', ThesisViewSet, basename='thesis')
 
urlpatterns = [
    path('', include(router.urls)), 
     
     ]
 
