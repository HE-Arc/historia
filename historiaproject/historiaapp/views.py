from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.contrib.auth.models import User
from .models import *


#|----------------------------------------------------------------------------|
#   Methods                                                                   |
#|----------------------------------------------------------------------------/

def home(request):
    """_summary_
    To display the main page with the possibility to register or login.
    Args:
        generic (_type_): _description_
    """
    context = {}
    return render(request, 'historiaapp/home.html', context)


#|----------------------------------------------------------------------------| 
#   Views Classes                                                             |
#|----------------------------------------------------------------------------/

#|-----------------------|
#| User, Login, Register |
#|-----------------------/

  
class AuthenticationForm(AuthenticationForm):
    """_summary_
    Form for the authentication form.
    Args:
        generic (_type_): AuthenticationForm from django _description_
    """
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            # Remove the help text
            self.fields[fieldname].help_text = None


class UserCreationForm(UserCreationForm):
    """_summary_
    Form to create a user with the form.
    Args:
        generic (_type_): UserCreationForm from django _description_
    """
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            # Remove the help text
            self.fields[fieldname].help_text = None


def login_view(request):
    """_summary_
    Display the login page.
    Args:
        generic (_type_): _description_
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            context = {}
            context['user'] = User.objects.get(username=request.POST.get("username"))
            return redirect('dashboard')
        else:
            context = {'form':form}
            context['form_errors'] = "Please enter a correct username and password."
            return render(request, "historiaapp/login.html", context)
    else:
        form = AuthenticationForm()  # Create a new instance of this form
    # Send the AuthenticationForm to render
    return render(request, "historiaapp/login.html", {'form': form})
    

def register_view(request):
    """_summary_
    Display the register page.
    Args:
        generic (_type_): _description_
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        # Pass information from form with request.POST
        context = {}
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('login')
        else:
            context = {'form':form}
            context['form_errors'] = "Please enter a correct username and password."
            return render(request, 'historiaapp/register.html', context)
    else:
        form = UserCreationForm()  # Create a new instance of this form
    # Send the UserCreationForm to render
    return render(request, "historiaapp/register.html", {'form': form})


@login_required(login_url="login")
def logout_view(request):
    """_summary_
    Logout the current user.
    Must be connected.
    Args:
        generic (_type_): _description_
    """
    logout(request)
    return redirect('home')



#|-----------------------|
#| Dashboard             |
#|-----------------------/


class DashboardView(generic.TemplateView):
    """_summary_
    Display dashboard.
    Must be connected.
    Args:
        generic (_type_): Template View _description_
    """
    template_name = "historiaapp/dashboard.html"
    
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs) 
            context['quizzes'] = Quiz.objects.all()
            context['cards'] = Card.objects.all()
            context['questions'] = Question.objects.all()
            return context
        else:
            context = {}
            return context


#|-----------------------|
#| Cards                 |
#|-----------------------/


class CardsListView(generic.ListView):
    """_summary_
    Function to display all cards in list.
    Args:
        generic (_type_): List View _description_
    """
    model = Card
    
    def get_queryset(self):
        return Card.objects.all()

class CardsDetailView(generic.DetailView):
    """_summary_
    Function to display details of one card.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Card

class CardsCreateView(generic.CreateView):
      
    model = Card
    fields = ['name',
                'historicPeriod',
                'domain',
                'category',
                'birth',
                'land',
                'image', 
                'text']
    
    success_url = reverse_lazy('cards-list')
    

class CardsUpdateView(generic.UpdateView):
    
    model = Card
    fields = ['name',
                'historicPeriod',
                'domain',
                'category',
                'birth',
                'land',
                'image', 
                'text']
    
    success_url = reverse_lazy('cards-list')
    
class CardsDeleteView(generic.DeleteView):
    
    model = Card
    success_url = reverse_lazy('cards-list')
    

#|-----------------------|
#| Quiz                  |
#|-----------------------/


class QuizView(generic.TemplateView):
    """_summary_
    Function to display all quiz.
    Must be connected.
    Args:
        generic (_type_): Template View _description_
    """
    
    template_name = "historiaapp/quiz.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.all()
        return context


class QuizListView(generic.ListView):
    """_summary_
    Function to display all quiz in a list.
    Args:
        generic (_type_): List View _description_
    """
    
    paginate_by = 2
    
    def get_queryset(self):
        quizs = Quiz.objects.all()
        for quiz in quizs:
            for question in quiz.questions.all():
                question.is_correct = False
                question.save()
                
        return quizs


class QuizDetailView(generic.DetailView):
    """_summary_
    Function to display one quiz with his details.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Quiz


class QuizCreateView(generic.CreateView):
    """_summary_
    To create a quiz in the database.
    Args:
        generic (_type_): _description_
    """
    model = Quiz
    
    fields = [
        'name',
        'text',
        'questions',
        'is_over'
    ]
    
    success_url = reverse_lazy('quizs-list')


class QuizUpdateView(generic.UpdateView):
    """_summary_
    To update a quiz in the database.
    Called from the quiz_update page -> <pk>/update route.
    Args:
        generic (_type_): _description_
    """
    model = Quiz

    fields = [
        'name', 
        'text', 
        'questions',
        'is_over'
    ]
    
    success_url = reverse_lazy('quizs-list')


class QuizDeleteView(generic.DeleteView):
    """_summary_
    To delete a question from the database.
    Called from the quiz_delete -> <pk>/delete route.
    Args:
        generic (_type_): _description_
    """
    model = Quiz
    success_url = reverse_lazy('quizs-list')

    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        quiz = Quiz.objects.get(pk=request.POST.get("quiz_id"))        
        quiz.delete()


class QuizCheckView(View):
    
    def post(self, request):
        """
        _summary_
        To check the posted answers through the form
        :param request: The HTTP request that is sent to the view
        :return: The quiz detail page.
        To check the posted answers through the form.
        Args:
            request (_type_): _description_
        Returns:
            _type_: _description_
        """
        quiz = Quiz.objects.get(pk=request.POST.get("quiz_id"))
        quiz.score = 0
        questions = quiz.questions.all()
        values = list(request.POST.values())
        values.pop(0)
        
        quiz.score_quiz = 0

        for question, answer in zip(questions, values):
            if answer == str(question.answer):
                quiz.score_quiz += 1
                question.is_correct = True
                question.save()
            else:
                question.is_correct = False
                question.save()
                
        print(quiz.score_quiz)
        
        quiz.score_quiz *= 100 / (len(values)-1)
        
        print(quiz.score_quiz)

        quiz.save()
        
        return redirect('quizs-detail', quiz.id)


#|-----------------------|
#| Questions             |
#|-----------------------/

class QuestionListView(generic.ListView):
    """ _summary_
    Function to display all questions of a quiz.
    Args:
        generic (_type_): List View _description_
    """
    model = Question
    def get_queryset(self):
        questions = Question.objects.all()
        
        return questions


class QuestionDetailView(generic.DetailView):
    """_summary_
    To show a question detail informations.
    Args:
        generic (_type_): Detail View _description_
    """
    model = Question


class QuestionCreateView(generic.CreateView):
    """_summary_
    To create a question in the database.
    Called from the question_create page -> <pk>/create route.
    Args:
        generic (_type_): Create View _description_
    """
    model = Question

    fields = [
        'name', 
        'text', 
        'opt_one',
        'opt_two',
        'opt_three',
        'opt_four',
        'answer',
        'character'
    ]
    
    success_url = reverse_lazy('questions-list')


class QuestionUpdateView(generic.UpdateView):
    """_summary_
    To update a question in the database.
    Called from the question_update page -> <pk>/update route.
    Args:
        generic (_type_): _description_
    """
    model = Question

    fields = [
        'name', 
        'text', 
        'opt_one',
        'opt_two',
        'opt_three',
        'opt_four',
        'answer',
        'character'
    ]
    
    success_url = reverse_lazy('questions-list')


class QuestionDeleteView(generic.DeleteView):
    """_summary_
    To delete a question from the database.
    Called from the question_delete -> <pk>/delete route.
    Args:
        generic (_type_): _description_
    """
    model = Question
    success_url = reverse_lazy('questions-list')

    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        question = Question.objects.get(pk=request.POST.get("question_id"))        
        question.delete()    


class QuestionCheckView(View):
    def post(self, request):
        """_summary_
        To check the posted answers through the form.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        question = Question.objects.get(pk=request.POST.get("question_id"))
        option = request.POST.get("option_id")

        if option == str(question.answer):
            question.is_correct = True
        else:
            question.is_correct = False

        question.save()
        
        return redirect('questions-list')


#|-----------------------|
#| Ranking               |
#|-----------------------/

class RankingListView(generic.ListView):
    """_summary_
    Function to display all rankings in a specific quiz.
    Must be connected.
    Args:
        generic (_type_): List View _description_
    """
    model = Ranking
    
    def get_queryset(self):
        return Ranking.objects.filter(quiz=1).order_by("-score")[:5]


def rankings_user(request):
    context = {}
    context['rankings'] = Ranking.objects.filter(user=request.user).order_by("-score")
    return render(request, "historiaapp/home.html", context) 
    