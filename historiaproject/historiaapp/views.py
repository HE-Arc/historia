from re import T

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from rest_framework import viewsets
from django.db.models.query import QuerySet
from typing import Generic

from .models import *
from django.contrib.auth import get_user_model



#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def home(request):
    context = {}
    return render(request, 'historiaapp/home.html', context)
    
def login(request):
    context = {}
    return render(request, 'historiaapp/login.html', context)

def signin(request):
    context = {}
    return render(request, 'historiaapp/signin.html', context)



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
    template_name = "historiaapp/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
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

# not used anymore, was mainly used to test data at first
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
