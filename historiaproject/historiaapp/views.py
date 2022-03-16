from re import T

from django.shortcuts import render
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

from .models import User
from .forms import AddQuestionForm
from .models import *

#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def index(request):
    context = {}
    return render(request, 'historiaapp/login.html', context)
    
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
    
#|----------------------------------------------------------------------------| 
#   Views Classes                                                             |
#|----------------------------------------------------------------------------/


#|-----------------------|
#| User, Login, Register |
#|-----------------------/

class RegisterView(generic.TemplateView):
    print("Register view")
    template_name = "historiaapp/register.html"
    
class HomePage(View):
    def get(self, request):
        return render(request, 'historiaapp/home.html', context)

my_default_errors = {
    'required': 'All the field are required. The passwords habe to be the same.',
    'invalid': 'Enter a valid value'
}

class MyForm(forms.ModelForm):
    name = forms.CharField()
    
    class Meta:
        model = User
        fields = ('pseudo', 'password')
        pseudo = forms.CharField(error_messages=my_default_errors)
        password = forms.CharField(error_messages=my_default_errors)

    
def AddUser(request):
    print("AddUser")
    context = {}
    if request.method == "POST" or None:
        pseudo = request.POST['pseudo']
        password = request.POST['password']
        passwordConfirm = request.POST['confirm_password']
        print(pseudo)
        print(password)
        print(passwordConfirm)
        
        if pseudo is not None and password == passwordConfirm:
            #template_name = "historiaapp/home.html"
            return render(request, 'historiaapp/home.html', context)
        else:
            form = MyForm(request.POST or None)
            print(form.errors)
            return render(request, 'historiaapp/register.html',{'form':form})

            #return render(request, 'historiaapp/register.html', context)
            #template_name = "historiaapp/register.html"
            
        '''
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            success_url = reverse_lazy('home')
            #template_name = "historiaapp/home.html"
        else:
            # Return an 'invalid login' error message.
            print(form.errors)
            
            
        form = MyForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            print(form)
            print("Valid form")
            form.save()
            template_name = "historiaapp/home.html"
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            template_name = "historiaapp/register.html"
    '''
    
    #model = User 
    #fields = ['username', 'password']
    #success_url = reverse_lazy('home')
    '''
    def post(self, request):  
        print("addUser")
        print(request)
        model = User 
        fields = ['username', 'password']
        
        pseudo = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            success_url = reverse_lazy('home')
            #template_name = "historiaapp/home.html"
        else:
            # Return an 'invalid login' error message.
            print(form.errors)
    
    def get(self, request):
        return HttpResponse('Unauthorized! AddUser.', status=401)
    '''

#|-----------------------|
#|Cards and Quizzes      |
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

class CardsListView(generic.ListView):
    model = Card
    
    # always use .objects when using the model 
    # in the view (controller)
    
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()
