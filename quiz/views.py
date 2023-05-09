from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserLoginForm
from .models import QuizUsers, Question, QuestionsAnswered, Category, ChooseAnswer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from decimal import Decimal


def index(request):

    context = {
        'welcome': 'Welcome',
    }

    return render(request, 'index.html', context)


def HomeUser(request):
    categories = Category.objects.all()
    questions = Question.objects.all()
    context = {
        'categories': categories,
        'questions': questions
    }

    return render(request, 'users/home.html', context)

def action(request):
    choose_category = request.POST.get('category')
    if not choose_category:
        return HttpResponse('Category cannot be null')
    category_name=Category.objects.filter(id=choose_category).values_list('id', 'name').first()
    validate_categorys=QuizUsers.objects.filter(users=request.user).values_list('choose_category')
    for category in validate_categorys:
        if str(category[0])==choose_category:
            return redirect('HomeUser')
    QuizUser, created = QuizUsers.objects.get_or_create(users=request.user, choose_category=choose_category)
    category_questions = Question.objects.filter(category_id=QuizUser.choose_category).values()
    choose_Answers_questions=ChooseAnswer.objects.all()
    anwers_options={}
    selected_answers = {}
    category_questions = list(category_questions) 
    for question in category_questions:
        question_id = question['id']
        choose_Answers_questions=ChooseAnswer.objects.filter(question_id=question_id).values_list('id', 'text')
        anwers_options[question_id] = list(choose_Answers_questions)
        answer_value = request.POST.get('answer_' + str(question['id']))
        if question_id in anwers_options:
            question['answers'] = anwers_options[question_id]
        if answer_value is not None:
            selected_answers[question_id] = answer_value
            question_answered, created = QuestionsAnswered.objects.update_or_create(
                quiz_user=QuizUser,
                question_id=question_id,
                defaults={'selected_answer_id': answer_value}
            )
    context = {
        'category_id': choose_category,
        "category_questions": category_questions,
        'category_name': category_name,
        'anwers_options': anwers_options,
        'answer_value': answer_value,
        'selected_answers': selected_answers
        }
    return render(request, 'play/action.html', context)

def panel(request):
    if request.method == 'POST':
        category_questions = Question.objects.filter(category_id=request.POST['category_id'])
        total_questions = len(category_questions)
        user = QuizUsers.objects.filter(users=request.user).last()
        if 'finish_button' in request.POST:
            for question in category_questions:
                answer_key = 'answer_{}'.format(question.id)
                selected_option_id = int(request.POST.get(answer_key, ''))
                selected_answer = ChooseAnswer.objects.get(pk=selected_option_id)
                category_id=request.POST['category_id']
                #correct_option = ChooseAnswer.objects.get(id=selected_answer.id)
                
                if selected_answer.correct is True:
                    obtained_score = selected_answer.question.max_score
                else:
                    obtained_score = 0
                QuestionsAnswered.objects.create(
                    question=question,
                    quizUser=user,
                    category=category_id,
                    answer=selected_answer,
                    obtained_score=obtained_score
                )
                total_score = QuestionsAnswered.objects.filter(quizUser=user).aggregate(Sum('obtained_score'))['obtained_score__sum']
                user.total_score=Decimal(str(total_score))
                user.save()
            return redirect('panel') 
    else:
        total_user_quiz = QuizUsers.objects.order_by('-total_score')[:10]
        counter = total_user_quiz.count()
        context = {
            'users_quiz': total_user_quiz,
            'count_user': counter
        }
        return render(request, 'play/panel.html', context)
    return redirect('panel')  

def loginView(request):
    title = 'HomeUser'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        users = authenticate(username=username, password=password)
        login(request, users)
        return redirect('HomeUser')

    context = {
        'form': form,
        'title': title,

    }

    return render(request, 'users/login.html', context)


def register(request):

    title = 'Create an account'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {

        'form': form,
        'title': title

    }

    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

def contact(request):
    return render(request, 'contact.html')

