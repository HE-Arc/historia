from unicodedata import name
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from django.urls import include

from . import views
from rest_framework import routers
from .models import Card
from .forms import AddQuestionForm, QuestionOptionsForm

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    
    path('cards/', views.CardsListView.as_view(), name='cards-list'),  
    
    path('cards/visualizer/', views.cards_visualizer, name='cards-visualizer'),
    
    path('questions/', views.QuestionListView.as_view(), name="questions-list"),
    
    path('questions/options', views.options_view, name='options'),
    
    path('login/', views.login, name='login'),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('home/', views.HomePage.as_view(), name='home'),
    
    path('user/add-user/', views.AddUser.as_view(), name='add-user'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)