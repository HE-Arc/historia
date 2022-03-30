from django.contrib.auth.models import User
from .models import Card, Question, Quiz

from rest_framework import serializers


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
            'opt_one',
            'opt_two',
            'opt_three',
            'opt_four',
            'answer',
            'options',
            'character'
        )


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = ('name', 'size', 'questions')
