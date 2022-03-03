from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

# Create your views here.

def index(request):
    context = {}
    return render(request, 'historiaapp/index.html', context)

#class RegisterView(generic.TemplateView):
#    template_name = "historiaapp/register.html"

class HomePage(View):
    def get(self, request):
        return render(request, 'historiaapp/home.html', context)


class AddUser(View):
    def post(self, request):
        print("ADD USER")
        return redirect('home')
    
    def get(self, request):
        return HttpResponse('Unauthorized! AddUser.', status=401)


