from unicodedata import name
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from django.urls import include

from . import views
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # User urls
    # ---------------------------------------------------------------------------------- #
        
    path('login/', views.login, name='login'),

    path('register/', views.RegisterView.as_view(), name='register'),
        
    path('user/add-user/', views.AddUser.as_view(), name='add-user'),
    
    # Cards urls
    # ---------------------------------------------------------------------------------- #
    
    path('dashboard/cards/', views.CardsListView.as_view(), name='cards-list'),  
        
    path('dashboard/cards/<pk>/', views.CardsDetailView.as_view(), name='cards-detail'),
    
    # Questions urls
    # ---------------------------------------------------------------------------------- #
    
    path('dashboard/questions/', views.QuestionListView.as_view(), name="questions-list"),
    
    path('dashboard/questions/check/', views.QuestionCheckView.as_view(), name="questions-check"),
        
    path('dashboard/questions/new/', views.QuestionCreateView.as_view(), name="questions-create"),
    
    path('dashboard/questions/<pk>/', views.QuestionDetailView.as_view(), name="questions-detail"),
    
    path('dashboard/questions/<pk>/update', views.QuestionUpdateView.as_view(), name="questions-update"),
    
    path('dashboard/questions/<pk>/delete', views.QuestionDeleteView.as_view(), name="questions-delete"),

    # Quiz urls
    # ---------------------------------------------------------------------------------- #
    
    path('dashboard/quiz/', views.QuizListView.as_view(), name="quizs-list"),
    
    path('dashboard/quiz/check/', views.QuizCheckView.as_view(), name="quizs-check"),
            
    path('dashboard/quiz/new/', views.QuizCreateView.as_view(), name="quizs-create"),
    
    path('dashboard/quiz/<pk>', views.QuizDetailView.as_view(), name="quizs-detail"),
    
    path('dashboard/quiz/<pk>/update', views.QuizUpdateView.as_view(), name="quizs-update"),
    
    path('dashboard/quiz/<pk>/delete', views.QuizDeleteView.as_view(), name="quizs-delete"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)