from re import T

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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



from .forms import *
from .models import *

#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def index(request):
    context = {}
    return render(request, 'historiaapp/login.html', context)

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
  
def login_view(request):
    if request.method == "POST":
        # Pass information from form with request.POST
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  # Check if form is valid or not (User exist ? Password ok ? etc.)
            user = form.get_user()
            login(request, user)
            context = {'form':form}
            return render(request, 'historiaapp/quiz.html', context)
        else:
            return redirect('historiaapp/login.html')
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
        return render(request, 'historiaapp/quiz.html', context)
    else:
        form = UserCreationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "historiaapp/register.html", {'form': form})

      
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')      


#|-----------------------|
#|Cards and Quizzes      |
#|-----------------------/

@login_required(login_url="login")
class CardsView(generic.TemplateView):
    template_name = "historiaapp/cards.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Card.objects.all()
        return context

@login_required(login_url="login")
class QuizView(generic.TemplateView):
    template_name = "historiaapp/quiz.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.all()
        return context

@login_required(login_url="login")
class CardsListView(generic.ListView):
    model = Card
    
    # always use .objects when using the model 
    # in the view (controller)
    
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()
