from django.forms import *
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import *

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

#|----------------------------------------------------------------------------| 
#   Model Forms                                                               |
#|----------------------------------------------------------------------------/

OPTIONS = [
        (1, 'one'),
        (2, 'two'),
        (3, 'three'),
        (4, 'four')
    ] 

class QuestionOptionsForm(ModelForm):

    options = CharField(widget=RadioSelect(choices=OPTIONS))
    
    class Meta:
        model = Question
        fields = '__all__'


class AddQuestionForm(ModelForm):
    """_summary_

    Args:
        ModelForm (_type_): _description_
    """
    class Meta:
        model = Quiz
        fields = "__all__"


class QuizzForm(ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"        
