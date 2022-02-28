from django.db import models


class Question(models.Model):
    quiz_id = models.ForeignKey('QuestionsByQuiz', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    
class Quiz(models.Model):
    text = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    size = models.IntegerField
    
class QuestionByQuiz(models.Model):
    question_id = models.ManyToManyField('Question')
    quiz_id = models.ManyToManyField('Quiz')
    
class AnswerOptions(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    answerText = models.CharField(max_length=200)
    isCorrect = models.BooleanField

class Score(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)
    
class Answer(models.Model):
    score_id = models.ManyToManyField('Score')
    answer_option_id = models.ManyToManyField('AnswerOptions')
    
class User(models.Model):
    pseudo = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    isAdmin = models.BooleanField
