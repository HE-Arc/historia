import json

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    context = {}
    return render(request, 'historiaapp/cards.html', context)

#class RegisterView(generic.TemplateView):
#    template_name = "historiaapp/register.html"


        
