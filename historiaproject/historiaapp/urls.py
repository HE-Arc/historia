from unicodedata import name
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from django.urls import include

from . import views
from rest_framework import routers
from .models import Card
from .forms import AddQuestionForm

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('cards/', views.CardsListView.as_view(), name='cards-list'),  
    
    path('cards/visualizer/', views.cards_visualizer, name='cards-visualizer'),
    
    path('quiz/', AddQuestionForm, name="quiz"),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
