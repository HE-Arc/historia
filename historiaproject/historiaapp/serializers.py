################################################################################
#                                                                              #
# Description : This file contains all serializers for models                  #
# Authors     : Simon Meier, Alex Mozerski and Yasmine Margueron               #
# Date        : 14.04.2022                                                     #
#                                                                              #
################################################################################


from .models import Card, Question, Quiz
from rest_framework import serializers

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = (
            'name',
            'historicPeriod',
            'domain',
            'category',
            'birth',
            'land',
            'text',
            'image'
        )


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
            'is_correct',
            'character'
        )


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            'name',
            'text',
            'questions',
            'score_quiz'
        )
