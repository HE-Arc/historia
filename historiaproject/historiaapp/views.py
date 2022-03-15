from re import T

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from rest_framework import viewsets
from django.db.models.query import QuerySet
from typing import Generic

from .forms import AddQuestionForm, QuestionOptionsForm
from .models import *

#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def index(request):
    context = {}
    return render(request, 'historiaapp/home.html', context)
    
def login(request):
    context = {}
    return render(request, 'historiaapp/login.html', context)
    
def cards_visualizer(request):
    context = {}
    return render(request, 'historiaapp/cards.html', context)    

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

def options_view(request):
    print(request)
    OptionsForm = QuestionOptionsForm(request.POST)
    if request.method == 'POST':
        answer = OptionsForm.cleaned_data['options']
    return render(request, "questions", {"answer" : answer})

#|----------------------------------------------------------------------------| 
#   Views Classes                                                             |
#|----------------------------------------------------------------------------/


#|-----------------------|
#| User, Login, Register |
#|-----------------------/

class RegisterView(generic.TemplateView):
    print("Register view")
    #model = User 
    #fields = ['username', 'password']
    #success_url = reverse_lazy('home')
    template_name = "historiaapp/register.html"
    
    #def get(self, request):
    #    return render(request, 'historiaapp/register.html', context)

class HomePage(View):
    def get(self, request):
        return render(request, 'historiaapp/home.html', context)

class AddUser(View):
    def post(self, request):
        print("ADD USER")
        return redirect('home')
    
    def get(self, request):
        return HttpResponse('Unauthorized! AddUser.', status=401)


#|-----------------------|
#| Cards and Quizzes     |
#|-----------------------/


class CardsView(generic.TemplateView):
    template_name = "historiaapp/cards.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Card.objects.all()
        return context


class QuizView(generic.TemplateView):
    template_name = "historiaapp/quiz.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.all()
        return context


class QuestionView(generic.TemplateView):
    template_name = "historiaapp/questions.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        return context


class QuestionListView(generic.ListView):
    model = Question  
      
    def get_queryset(self) -> QuerySet[T]:
        return Question.objects.all()


class CardsListView(generic.ListView):
    model = Card    
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()
