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
    context = {}
    return render(request, 'historiaapp/home.html', context)

@login_required(login_url="login")    
def cards_visualizer(request):
    context = {}
    return render(request, 'historiaapp/cards.html', context)    

@login_required(login_url="login")
def add_question(request):
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
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

class HomePage(View):
    template_name = "historiaapp/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
def login_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.get_user()
            login(request, user)
            context = {'form':form}
            
            return render(request, 'quiz-list', context)
        else:
            return redirect('login')
    else:
        form = AuthenticationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "historiaapp/login.html", {'form': form})
    
    
def register_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
        context = {'form':form}
        return render(request, 'historiaapp/quiz_list.html', context)
    else:
        form = UserCreationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "historiaapp/register.html", {'form': form})

@login_required(login_url="login")  
def logout_view(request):
    logout(request)
    return redirect('login')
   


#|-----------------------|
#| Dashboard             |
#|-----------------------/

class DashboardView(generic.TemplateView):
    template_name = "historiaapp/dashboard.html"


@login_required(login_url="login")
class CardsView(generic.TemplateView):
    template_name = "historiaapp/cards.html"
    

def get_context_data(self, **kwargs):
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
    model = Card    
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()


class CardsDetailView(generic.DetailView):
    model = Card



#|-----------------------|
#| Quiz                  |
#|-----------------------/

# not used anymore, was mainly used to test data at first

@login_required(login_url="login")
class QuizView(generic.TemplateView):
    template_name = "historiaapp/quiz.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.all()
        return context

class QuizListView(generic.ListView):
    model = Quiz
    def get_queryset(self) -> QuerySet[T]:
        return Quiz.objects.all()


class QuizDetailView(generic.DetailView):
    model = Quiz



#|-----------------------|
#| Questions             |
#|-----------------------/

# not used anymore, was mainly used to test data at first
class QuestionView(generic.TemplateView):
    template_name = "historiaapp/question_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        return context


class QuestionListView(generic.ListView):
    model = Question
    def get_queryset(self) -> QuerySet[T]:
        return Question.objects.all()


class QuestionDetailView(generic.DetailView):
    """_summary_
    To show a question detail informations.
    Args:
        generic (_type_): _description_
    """
    model = Question


class QuestionCreateView(generic.CreateView):
    """_summary_
    To create a question in the database.
    Called from the question_create page -> <pk>/create route.
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
#| Ranking             |
#|-----------------------/

def DateNow():
    return datetime.datetime.utcnow().replay(tzinfo=utc)



class RankingListView(generic.ListView):
    model = Ranking
    
    def get_queryset(self) -> QuerySet[T]:
        return Ranking.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last'] = Ranking.objects.order_by("-score")[:5]
        return context
  
class RankingDetailView(generic.DetailView):
    model = Ranking
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last'] = Ranking.objects.order_by("-score")[:5]
        return context
    
    
    