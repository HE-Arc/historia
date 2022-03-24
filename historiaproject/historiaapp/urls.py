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
        
    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register_view, name='register'),
    
    
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
    
    path('dashboard/questions/', views.QuestionListView.as_view(), name="questions-list"),
    
    path('dashboard/questions/check/', views.QuestionCheckView.as_view(), name="questions-check"),
        
    path('dashboard/questions/new/', views.QuestionCreateView.as_view(), name="questions-create"),
    
    path('dashboard/questions/<pk>/', views.QuestionDetailView.as_view(), name="questions-detail"),
    
    path('dashboard/questions/<pk>/update', views.QuestionUpdateView.as_view(), name="questions-update"),
    
    path('dashboard/questions/<pk>/delete', views.QuestionDeleteView.as_view(), name="questions-delete"),


    # Ranking urls
    # ---------------------------------------------------------------------------------- #
    
    path('ranking/<pk>', views.RankingDetailView.as_view(), name="ranking"),
     
    path('rankings/', views.RankingListView.as_view(), name="ranking-list"),

    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)