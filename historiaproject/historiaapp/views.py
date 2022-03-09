import json
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
from .models import Card


def index(request):
    context = {}
    return render(request, 'historiaapp/index.html', context)
    
def cards_visualizer(request):
    context = {}
    return render(request, 'historiaapp/cards.html', context)    

class CardsView(generic.TemplateView):
    template_name = "historiaapp/cards.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Card.objects.all()
        return context
    
class CardsListView(generic.ListView):
    model = Card
    
    # always use .objects when using the model 
    # in the view (controller)
    
    def get_queryset(self) -> QuerySet[T]:
        return Card.objects.all()
