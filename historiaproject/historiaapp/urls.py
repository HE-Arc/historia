from django.urls import path
from django.contrib import admin

from . import views

# TODO-ADV-1-3 Add a rest_framework router to register the 2 new viewsets that you've created


urlpatterns = [
    path('', views.index, name='index'),
    #path('register/', views.RegisterView, name='register')
]