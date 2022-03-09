from django.contrib.auth.models import User
from .models import Card

from rest_framework import serializers

# serializers : permet de récuperé des modèles et de les retourner en fichiers json

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ('name', 'image', 'birth', 'text')
