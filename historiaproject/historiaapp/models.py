from django.db import models
from django.core import serializers


class AnswerOptions(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    answerText = models.CharField(max_length=200)
    isCorrect = models.BooleanField(default=False)

class Score(models.Model):
    #user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)

  
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
    image = models.ImageField(upload_to='images/', null=True)
    birth = models.CharField(max_length=20)
    text = models.CharField(max_length=4000)
    
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