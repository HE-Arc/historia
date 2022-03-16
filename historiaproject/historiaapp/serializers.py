from django.contrib.auth.models import User
from .models import Card, Question, Quiz

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


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = (
            'name', 
            'text', 
            'text_opt_one',
            'text_opt_two',
            'text_opt_three',
            'text_opt_four',
            'answer',
            'options',
            'character'
        )


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = ('name', 'size', 'questions')
