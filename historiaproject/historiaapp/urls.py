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
    path('cards_visualizer/', views.cards_visualizer, name='cards_visualizer'),
    path('add_question/', AddQuestionForm, name="add_question"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
