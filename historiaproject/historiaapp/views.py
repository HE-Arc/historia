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

def get_answer(request):
    
    form = QuestionOptionsForm()
    
    if request.method == 'POST':
        form = QuestionOptionsForm(request.POST)
        
        if form.is_valid():
            form.save()
            selected = form.cleaned_data.get('options')
            print(selected)
        
            return redirect('questions/')
        
        context={'form':form}
        
        return render(request, 
                'question_list.html', 
                context)
        
    else:
        return redirect('questions/')




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
#| Dashboard             |
#|-----------------------/

class DashboardView(generic.TemplateView):
    template_name = "historiaapp/dashboard.html"

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


class QuestionDetailView(generic.DetailView):
    model = Question
