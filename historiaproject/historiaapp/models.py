################################################################################
#                                                                              #
# Description : This file contains all models for this project                 #
# Authors     : Simon Meier, Alex Mozerski and Yasmine Margueron               #
# Date        : 14.04.2022                                                     #
#                                                                              #
################################################################################

from django.db import models
from django.conf import settings

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
    historicPeriod = models.CharField(max_length=400, default="Unknown")
    domain = models.CharField(max_length=200, default="Unknown")
    category = models.CharField(max_length=400, default="Unknown")
    birth = models.CharField(max_length=100, default="Unknown")
    land = models.CharField(max_length=200, default="Unknown")
    text = models.TextField(max_length=4000)
    image = models.ImageField(upload_to='images/', null=True)
    
    def __str__(self) -> str:
        return self.name

class Quiz(models.Model):
    """_summary_
    Quiz model based on a number of questions.
    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=200)
    text = models.TextField(max_length=2000)
    questions = models.ManyToManyField('Question', related_name="questions")
    score_quiz = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category")    
    
    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    """_summary_
    Question model four possible answers.
    opt_{N} corresponds to the texted answer showed to the user.
    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=200)
    text = models.TextField(max_length=2000)
    
    opt_one = models.CharField(max_length=200)
    opt_two = models.CharField(max_length=200)
    opt_three = models.CharField(max_length=200)
    opt_four = models.CharField(max_length=200)
    
    answer = models.IntegerField(default=1)
    is_correct = models.BooleanField(default=False)
    character = models.ForeignKey('Card', on_delete=models.CASCADE, null=True)
    options = models.IntegerChoices('Options', 'ONE TWO THREE FOUR')
    
    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """_summary_
    Category model with a name and an image. Category links to quiz.
    Args:
        models (_type_): _description_
    """
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/category/', null=True)

    
class Ranking(models.Model):
    """_summary_
    Model for ranking against a specific quiz and user.
    Args:
        models (_type_): _description_
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(db_index=True)
    
