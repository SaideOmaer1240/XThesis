
# In urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from django.urls import path
from .views import TopicViewSet, ThesisViewSet, DestroyAllTheses, DestroyOneThesis
router = DefaultRouter()

router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'theses', ThesisViewSet, basename='thesis')
 
urlpatterns = [
    path('', include(router.urls)), 
    path('delete/all/theses/', DestroyAllTheses.as_view(), name='destroy-theses'),
    path('delete/one/thesis/', DestroyOneThesis.as_view(), name='destroy-one-thesis'),
     
     ]
 
