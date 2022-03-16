from email.mime import image
import imp
from importlib.resources import path
from unicodedata import name
from django.db import models
from django.core import serializers
import json
from pprint import pprint 


class QuestionByQuiz(models.Model):
    question_id = models.ManyToManyField('Question')
    quiz_id = models.ManyToManyField('Quiz')

    
class AnswerOptions(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    answerText = models.CharField(max_length=200)
    isCorrect = models.BooleanField(default=False)


class User(models.Model):
    pseudo = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    isAdmin = models.BooleanField

    
class Score(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)

    
class Answer(models.Model):
    score_id = models.ManyToManyField('Score')
    answer_option_id = models.ManyToManyField('AnswerOptions')
    
    
class Card(models.Model):
    """_summary_
    Card model for historical characters registered in cards.json file.
    It is used as a reward when answering a question from a quizz.
    Args:
        models (_type_): Model

    Returns:
        _type_: Card
    """
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', default="")
    birth = models.CharField(max_length=20)
    text = models.CharField(max_length=4000)
    
    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    """_summary_
    Quiz model based on question with four possible answers.
    Args:
        models (_type_): _description_
    """            
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    
    opt_one = models.CharField(max_length=200)
    opt_two = models.CharField(max_length=200)
    opt_three = models.CharField(max_length=200)
    opt_four = models.CharField(max_length=200)

    answer = models.IntegerField(default=1)

    character = models.ForeignKey('Card', 
                                on_delete=models.CASCADE, 
                                null=True)

    options = models.IntegerChoices('Options', 
                                'ONE TWO THREE FOUR')

    def __str__(self) -> str:
        return self.name
    
    def get_answer(self) -> int:
        return self.answer
    

class Quiz(models.Model):
    """_summary_
    Quiz model based on question with four possible answers.
    Args:
        models (_type_): _description_
    """
    # name of the quiz
    name = models.CharField(max_length=200)
    
    # number of questions of the quiz
    size = models.IntegerField
    
    questions = [
        models.ForeignKey("Question", on_delete=models.CASCADE),
        models.ForeignKey("Question", on_delete=models.CASCADE),
        models.ForeignKey("Question", on_delete=models.CASCADE),
        models.ForeignKey("Question", on_delete=models.CASCADE)
    ]

    def __str__(self) -> str:
        return self.name
   