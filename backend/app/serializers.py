from rest_framework import serializers
from .models import Thesis 
class ThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = ['id','author', 'topic', 'title', 'text', 'date_added']
        read_only_fields = ['author']