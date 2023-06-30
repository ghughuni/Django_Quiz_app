from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserLoginForm
from .models import QuizUsers, Question, QuestionsAnswered, Category, ChooseAnswer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



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
    category_name = Category.objects.filter(
        id=choose_category).values_list('id', 'name').first()
    validate_categorys = QuizUsers.objects.filter(
        users=request.user).values_list('choose_category')
    QuizUser, created = QuizUsers.objects.get_or_create(
        users=request.user, choose_category=choose_category)
    category_questions = Question.objects.filter(
        category_id=QuizUser.choose_category).values()
    choose_Answers_questions = ChooseAnswer.objects.all()
    anwers_options = {}
    selected_answers = {}
    category_questions = list(category_questions)
    random.shuffle(category_questions)
    for question in category_questions:
        question_id = question['id']
        choose_Answers_questions = ChooseAnswer.objects.filter(
            question_id=question_id).values_list('id', 'text')
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
        if 'finish_button' in request.POST:
            category_questions = Question.objects.filter(
                category_id=request.POST['category_id'])
            category_name = Category.objects.filter(id=request.POST['category_id']).values_list('name').first()[0]
            user = User.objects.filter(username=request.user).values_list('id')
            user_email = User.objects.filter(username=request.user).values_list('email')[0][0]
            user_id = user[0][0]
            user = QuizUsers.objects.filter(
                users=user_id).values_list('id')[0][0]
            total_score = 0
            for question in category_questions:
                answer_key = 'answer_{}'.format(question.id)
                selected_option_id = int(request.POST.get(answer_key, ''))
                selected_answer = ChooseAnswer.objects.get(
                    pk=selected_option_id)
                category_id = request.POST['category_id']

                if selected_answer.correct is True:
                    obtained_score = selected_answer.question.max_score
                else:
                    obtained_score = 0
                question_answered = QuestionsAnswered.objects.filter(
                    question=question,
                    quizUser=user,
                    category=category_id
                ).first()

                if question_answered:
                    if obtained_score > question_answered.obtained_score:
                        question_answered.answer = selected_answer
                        question_answered.obtained_score = obtained_score
                        question_answered.save()
                else:
                    QuestionsAnswered.objects.create(
                        question=question,
                        quizUser=user,
                        category=category_id,
                        answer=selected_answer,
                        obtained_score=obtained_score
                    )
                total_score += obtained_score
                total_score = QuestionsAnswered.objects.filter(
                    quizUser=user, category=request.POST['category_id']).aggregate(Sum('obtained_score'))['obtained_score__sum']
                this_user = QuizUsers.objects.get(
                    users=user_id, choose_category=request.POST['category_id'])
                this_user.total_score = total_score
                this_user.save()
            send_mail(
                'Quiz Result',
                '''Congratulations! 

You have finished the {} quiz. Your total score is {}.

You can try again to improve your score and get on the leaderboard, or try another category quiz.

Good Luck...'''.format(category_name,total_score),
                settings.DEFAULT_FROM_EMAIL,  
                [user_email],  
                fail_silently=False,
            )

            return redirect('panel')
        if 'filter_button' in request.POST:
            category_id = request.POST.get('category_id', None)
        if category_id:
            user_scores = QuizUsers.objects.filter(
                choose_category=category_id
            ).order_by('-total_score')[:10]
        else:
            user_scores = QuizUsers.objects.order_by('-total_score')[:10]

        count_user = user_scores.count()
        categories = Category.objects.all()
        context = {
            'users_quiz': user_scores,
            'count_user': count_user,
            'categories': categories,
        }
        return render(request, 'play/panel.html', context)

    else:
        categories = Category.objects.all()
        total_user_quiz = QuizUsers.objects.order_by('-total_score')[:10]
        counter = total_user_quiz.count()
        context = {
            'users_quiz': total_user_quiz,
            'count_user': counter,
            'categories': categories,
        }
        return render(request, 'play/panel.html', context)


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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and email and password1 and password2):
            messages.error(request, 'Please fill out all fields')
            return render(request, 'users/register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'users/register.html')
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()
        # Send registration email
        send_mail(
            'Registration Successful',
            '''Thank you for registering on "GK-Quiz" website!

Get started today by visiting: ghughuni.pythonanywhere.com

Challenge yourself and learn something new!''',
            settings.DEFAULT_FROM_EMAIL,  
            [email],  
            fail_silently=False,
        )
        return redirect('login')
    else:
        return render(request, 'users/register.html', {'title': title})


def logout_view(request):
    logout(request)
    return redirect('/')


def contact(request):
    return render(request, 'contact.html')


def results(request):
    user_id = request.user.id
    user_quiz = QuizUsers.objects.filter(users=user_id).values()
    try:
        messages = None
        quiz_User = int(user_quiz[0]['id'])
        category_id = request.POST.get('category_id')
        if category_id:
            category_questions = Question.objects.filter(
                category_id=category_id).values()
            questions = []
            for question in category_questions:
                answered = QuestionsAnswered.objects.filter(
                    quizUser=quiz_User, category=category_id, question=question['id']).values()
                question_text = question['text']
                if answered:
                    user_answered = ChooseAnswer.objects.filter(
                        id=answered[0]['answer_id']).values_list('text')[0][0]
                    correct_answer = ChooseAnswer.objects.filter(
                        question=question['id'], correct=True).values_list('text')[0][0]
                    score = answered[0]['obtained_score']
                else:
                    question_text = '-'
                    user_answered = '-'
                    correct_answer = '-'
                    score = 0

                questions.append({
                    'question_text': question_text,
                    'answer': user_answered,
                    'correct_answer': correct_answer,
                    'score': score
                })
            category_name = Category.objects.get(id=category_id).name
            try:
                total_score = QuizUsers.objects.filter(
                    users=user_id, choose_category=category_id).values_list('total_score')[0][0]
            except:
                total_score = 0
            context = {
                'questions': questions,
                'total_score': total_score,
                'categories': Category.objects.all(),
                'selected_category_id': category_id,
                'category_name': category_name,
            }
            return render(request, 'users/results.html', context)

        context = {
            'categories': Category.objects.all(),
        }
        return render(request, 'users/results.html', context)
    except:
        messages = 'You have not taken any quiz yet.'
        context = {
            'messages': messages,
        }
        return render(request, 'users/results.html', context)
