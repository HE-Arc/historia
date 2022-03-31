from cgi import print_arguments
from re import T
from urllib import request

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

def cards_visualizer(request):
    """_summary_
    To display the page with the cards.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    context = {}
    return render(request, 'historiaapp/cards.html', context)  
    

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
            return render(request, "historiaapp/home.html", context)
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
        return render(request, 'historiaapp/home.html', context)
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

class CardsCreateView(generic.CreateView):
      
    model = Card
    fields = ['name',
              'image', 
              'birth',
              'text']
    
    success_url = reverse_lazy('cards-list')
    

class CardsUpdateView(generic.UpdateView):
    
    model = Card
    fields = ['name',
              'image', 
              'birth',
              'text']
    
    success_url = reverse_lazy('cards-list')
    
class CardsDeleteView(generic.DeleteView):
    
    model = Card
    success_url = reverse_lazy('cards-list')
    

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
    paginate_by = 2
    
    def get_queryset(self) -> QuerySet[T]:
        quizs = Quiz.objects.all()
        for quiz in quizs:
            for question in quiz.questions.all():
                question.is_correct = False
                question.save()
                
        return quizs


class QuizDetailView(generic.DetailView):
    """_summary_
    Function to display one quiz with his details.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Quiz


class QuizCreateView(generic.CreateView):
    """_summary_
    To create a quiz in the database.
    Args:
        generic (_type_): _description_
    """
    model = Quiz
    
    fields = [
        'name',
        'text',
        'questions',
        'is_over'
    ]
    
    success_url = reverse_lazy('quizs-list')


class QuizUpdateView(generic.UpdateView):
    """_summary_
    To update a quiz in the database.
    Called from the quiz_update page -> <pk>/update route.
    Args:
        generic (_type_): _description_
    """
    model = Quiz

    fields = [
        'name', 
        'text', 
        'questions',
        'is_over'
    ]
    
    success_url = reverse_lazy('quizs-list')


class QuizDeleteView(generic.DeleteView):
    """_summary_
    To delete a question from the database.
    Called from the quiz_delete -> <pk>/delete route.
    Args:
        generic (_type_): _description_
    """
    model = Quiz
    success_url = reverse_lazy('quizs-list')

    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        quiz = Quiz.objects.get(pk=request.POST.get("quiz_id"))        
        quiz.delete()


class QuizCheckView(View):
    
    def post(self, request):
        """
        _summary_
        To check the posted answers through the form
        :param request: The HTTP request that is sent to the view
        :return: The quiz detail page.
        To check the posted answers through the form.
        Args:
            request (_type_): _description_
        Returns:
            _type_: _description_
        """
        quiz = Quiz.objects.get(pk=request.POST.get("quiz_id"))
        quiz.score = 0
        questions = quiz.questions.all()
        values = list(request.POST.values())
        values.pop(0)
        
        quiz.score_quiz = 0

        for question, answer in zip(questions, values):
            if answer == str(question.answer):
                quiz.score_quiz += 1
                question.is_correct = True
                question.save()
            else:
                question.is_correct = False
                question.save()
                
        print(quiz.score_quiz)
        
        quiz.score_quiz *= 100 / (len(values)-1)
        
        print(quiz.score_quiz)

        quiz.save()
        
        return redirect('quizs-detail', quiz.id)


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
        questions = Question.objects.all()
        
        return questions


class QuestionDetailView(generic.DetailView):
    """_summary_
    To show a question detail informations.
    Args:
        generic (_type_): Detail View _description_
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
    
    success_url = reverse_lazy('questions-list')



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
    
    