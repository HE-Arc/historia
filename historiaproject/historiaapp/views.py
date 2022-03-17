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
    'required': 'All the field are required. The passwords have to be the same.',
    'invalid': 'Enter a valid value'
}

class AddUserForm(forms.ModelForm):  
    class Meta:
        model = User
        fields = "__all__"
        pseudo = forms.CharField(error_messages=my_default_errors)
        password = forms.CharField(error_messages=my_default_errors)

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['pseudo'].error_messages.update({
            'required': 'Please enter an username.',
        })
        
        self.fields['password'].error_messages.update({
            'required': 'The passwords have to be the same.',
        })
        
      
class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        pseudo = forms.CharField(error_messages=my_default_errors)
        password = forms.CharField(error_messages=my_default_errors)

  
def LoginUser(request):
    context = {}
    form = LoginUserForm(request.POST or None)
    pseudo = request.POST['pseudo']
    password = request.POST['password']
    
    user = authenticate(request, pseudo=pseudo, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        success_url = reverse_lazy('home')
    else:
        # Return an 'invalid login' error message.
        return render(request, 'historiaapp/login.html',{
            "message": "Wrong login" })
    
    
def AddUser(request):
    context = {}
    if request.method == "POST" or None:
        form = AddUserForm(request.POST or None)
        pseudo = request.POST['pseudo']
        password = request.POST['password']
        passwordConfirm = request.POST['confirm_password']
        
        if password == passwordConfirm and form.is_valid():
            form.save()
            return render(request, 'historiaapp/home.html', context)
        else:
            return render(request, 'historiaapp/register.html',{
            "message": "Passwords must match."
        })
            

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
