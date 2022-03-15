from django.forms import ChoiceField
from django.forms import ModelForm
from django.forms import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#/----------------------------------------------------------------------------\#   
#   _summary_:
#   
#   To access, update, create or delete entries in the database 
#   (to implement CRUD functionality), we need forms.
#   Form makes it easy to implement CRUD functionality as we neither have to 
#   create forms to accept information from users nor we have to validate 
#   information manually, we can just use is_valid() method to validate 
#   the information before updating it in the database.
#
#\----------------------------------------------------------------------------/#

# class CreateUserForm(UserCreationForm):
#     """_summary_
# 
#     Args:
#         UserCreationForm (_type_): _description_
#     """
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email') 
 

class QuestionOptionsForm(ModelForm):
    model = Question
    options = (
        model.ans_one,
        model.ans_two,
        model.ans_three,
        model.ans_four     
    )

    options= ChoiceField(choices = options)
    

class AddQuestionForm(ModelForm):
    """_summary_

    Args:
        ModelForm (_type_): _description_
    """
    class Meta:
        model = Quiz
        fields = "__all__"