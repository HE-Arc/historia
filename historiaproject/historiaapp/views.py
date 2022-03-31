from re import T

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from django.db.models.query import QuerySet
from typing import Generic
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.utils.timezone import utc
from optparse import make_option
from django.utils import timezone

from .forms import *
from .models import *
from django.contrib.auth import get_user_model



#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def home(request):
    """_summary_
    To display the main page with the possibility to register or login.
    Args:
        generic (_type_): _description_
    """
    context = {}
    return render(request, 'historiaapp/home.html', context)

@login_required(login_url="login")    
def cards_visualizer(request):
    """_summary_
    To display the page with the cards.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    context = {}
    return render(request, 'historiaapp/cards.html', context)    

@login_required(login_url="login")
def add_question(request):
    """_summary_
    To add question in a quiz.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    form = AddQuestionForm()
    if request.method=='POST':
        form = AddQuestionForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
        context = {'form':form}
        return render(request, 'add_question.html', context)
    else:
        return redirect('cards')
  
  

#|----------------------------------------------------------------------------| 
#   Views Classes                                                             |
#|----------------------------------------------------------------------------/

#|-----------------------|
#| User, Login, Register |
#|-----------------------/
  
class AuthenticationForm(AuthenticationForm):
    """_summary_
    Form for the authentication form.
    Args:
        generic (_type_): AuthenticationForm from django _description_
    """
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            # Remove the help text
            self.fields[fieldname].help_text = None


class UserCreationForm(UserCreationForm):
    """_summary_
    Form to create a user with the form.
    Args:
        generic (_type_): UserCreationForm from django _description_
    """
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            # Remove the help text
            self.fields[fieldname].help_text = None
            
            
def login_view(request):
    """_summary_
    Display the login page.
    Args:
        generic (_type_): _description_
    """
    if request.method == "POST":
        # Pass information from form with POST request
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  # Check if form is valid or not (User exists ? Password ok ?)
            user = form.get_user()
            login(request, user)
            context = {'form':form}
            # Redirect with the user's home with his rankings
            context['rankings'] = Ranking.objects.filter(user=request.user).order_by("-score")
            return render(request, "historiaapp/home_user.html", context)
        else:
            return redirect('login') # Redirect to login if form is not valid
    else:
        form = AuthenticationForm()  # Create a new instance of this form
    # Send the AuthenticationForm to render
    return render(request, "historiaapp/login.html", {'form': form})
    
    
def register_view(request):
    """_summary_
    Display the register page.
    Args:
        generic (_type_): _description_
    """
    if request.method == "POST":
        # Pass information from form with request.POST
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
        context = {'form':form}
        return render(request, 'historiaapp/home_user.html', context)
    else:
        form = UserCreationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "historiaapp/register.html", {'form': form})

@login_required(login_url="login")
def logout_view(request):
    """_summary_
    Logout the current user.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    logout(request)
    return redirect('login')


@login_required(login_url="login")    
def home_user_view(request):
    """_summary_
    Display the user's home page.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    context = {}
    context['rankings'] = Ranking.objects.filter(user=request.user).order_by("-score")
    return render(request, 'historiaapp/home_user.html', context)   



#|-----------------------|
#| Dashboard             |
#|-----------------------/


class DashboardView(generic.TemplateView):
    """_summary_
    Display dashboard.
    Must be connected.
    Args:
        generic (_type_): Template View _description_
    """
    template_name = "historiaapp/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.all()
        context['quizzes'] = Quiz.objects.all()
        context['cards'] = Card.objects.all()
        context['questions'] = Question.objects.all()
        return context


@login_required(login_url="login")
class CardsView(generic.TemplateView):
    """_summary_
    Display the card's page.
    Must be connected.
    Args:
        generic (_type_): Template View _description_
    """
    template_name = "historiaapp/cards.html"
    

def get_context_data(self, **kwargs):
    """_summary_
    Function to take all informations : user, quiz, card and question.
    Args:
        generic (_type_): _description_
    """
    context = super().get_context_data(**kwargs)
    context['user'] = User.objects.all()
    context['quizzes'] = Quiz.objects.all()
    context['cards'] = Card.objects.all()
    context['questions'] = Question.objects.all()
    return context



#|-----------------------|
#| Cards                 |
#|-----------------------/

class CardsListView(generic.ListView):
    """_summary_
    Function to display all cards in list.
    Args:
        generic (_type_): List View _description_
    """
    model = Card
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()


class CardsDetailView(generic.DetailView):
    """_summary_
    Function to display details of one card.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Card



#|-----------------------|
#| Quiz                  |
#|-----------------------/

@login_required(login_url="login")
class QuizView(generic.TemplateView):
    """_summary_
    Function to display all quiz.
    Must be connected.
    Args:
        generic (_type_): Template View _description_
    """
    template_name = "historiaapp/quiz.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.all() # Get all quiz
        return context


class QuizListView(generic.ListView):
    """_summary_
    Function to display all quiz in a list.
    Args:
        generic (_type_): List View _description_
    """
    model = Quiz
    def get_queryset(self) -> QuerySet[T]:
        return Quiz.objects.all() # Get all quiz


class QuizDetailView(generic.DetailView):
    """_summary_
    Function to display one quiz with his details.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Quiz



#|-----------------------|
#| Questions             |
#|-----------------------/

class QuestionListView(generic.ListView):
    """ _summary_
    Function to display all questions of a quiz.
    Args:
        generic (_type_): List View _description_
    """
    model = Question
    def get_queryset(self) -> QuerySet[T]:
        return Question.objects.all()


class QuestionDetailView(generic.DetailView):
    """_summary_
    To show a question detail informations.
    Args:
        generic (_type_): DEtail View _description_
    """
    model = Question


class QuestionCreateView(generic.CreateView):
    """_summary_
    To create a question in the database.
    Called from the question_create page -> <pk>/create route.
    Args:
        generic (_type_): Create View _description_
    """
    model = Question

    fields = [
        'name', 
        'text', 
        'opt_one',
        'opt_two',
        'opt_three',
        'opt_four',
        'answer',
        'character'
    ]


class QuestionUpdateView(generic.UpdateView):
    """_summary_
    To update a question in the database.
    Called from the question_update page -> <pk>/update route.
    Args:
        generic (_type_): _description_
    """
    model = Question

    fields = [
        'name', 
        'text', 
        'opt_one',
        'opt_two',
        'opt_three',
        'opt_four',
        'answer',
        'character'
    ]
    
    success_url = reverse_lazy('questions-list')


class QuestionDeleteView(generic.DeleteView):
    """_summary_
    To delete a question from the database.
    Called from the question_delete -> <pk>/delete route.
    Args:
        generic (_type_): _description_
    """
    model = Question
    success_url = reverse_lazy('questions-list')

    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        question = Question.objects.get(pk=request.POST.get("question_id"))        
        question.delete()    


class QuestionCheckView(View):
    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        question = Question.objects.get(pk=request.POST.get("question_id"))
        option = request.POST.get("option_id")

        if option == str(question.answer):
            question.is_correct = True
        else:
            question.is_correct = False

        question.save()
        
        return redirect('questions-list')


#|-----------------------|
#| Ranking               |
#|-----------------------/

class RankingListView(generic.ListView):
    """_summary_
    Function to display all rankings in a specific quiz.
    Must be connected.
    Args:
        generic (_type_): List View _description_
    """
    model = Ranking
    
    def get_queryset(self) -> QuerySet[T]:
        return Ranking.objects.filter(quiz=1).order_by("-score")[:5]
    
    