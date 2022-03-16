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
    
    path('', views.index, name='index'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # User urls
    # ---------------------------------------------------------------------------------- #
        
    path('login/', views.login, name='login'),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('home/', views.HomePage.as_view(), name='home'),
    
    path('user/add-user/', views.AddUser.as_view(), name='add-user'),
    
    # Cards urls
    # ---------------------------------------------------------------------------------- #
    
    path('dashboard/cards/', views.CardsListView.as_view(), name='cards-list'),  
        
    path('dashboard/cards/<pk>/', views.CardsDetailView.as_view(), name='cards-detail'),
    
    # Quiz urls
    # ---------------------------------------------------------------------------------- #
    
    path('dashboard/quiz/', views.QuizListView.as_view(), name="quiz-list"),
    
    path('dashboard/quiz/<pk>', views.QuizDetailView.as_view(), name="quiz-detail"),
    
    # Questions urls
    # ---------------------------------------------------------------------------------- #
    
    path('questions/', views.QuestionListView.as_view(), name="questions-list"),
    
    path('questions/<pk>', views.QuestionListView.as_view(), name="questions-detail"),
    
    path('get_answer/', views.get_answer, name='get_answer'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)