from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserLoginForm
from .models import QuizUsers, Question, QuestionsAnswered, Category


def index(request):

	context = {
		'welcome': 'Welcome',
	}

	return render(request, 'index.html', context)


def HomeUser(request):
	categories=Category.objects.all()
	category_id=request.GET.get('category')
	if category_id:
		print(category_id)
		return redirect('action')
	else:
		pass
	context = {
			'categories': categories,
		
		}
	
	return render(request, 'users/home.html', context)

def action(request):
	QuizUser, created = QuizUsers.objects.get_or_create(users=request.user)
	# category_questions=Question.objects.filter(id=category_id).values_list('text')
	# print(category_questions)
	if request.method == 'POST':
		# category_id = request.POST.get('category_id')
		# print(category_id)
		question_pk = request.POST.get('question_pk')
		question_answered = QuizUser.attempts.select_related('question').get(question__pk=question_pk)
		answer_pk = request.POST.get('answer_pk')
		try:
			selected_option = question_answered.question.options.get(pk=answer_pk)
			QuizUser.validate_attempts(question_answered, selected_option)
		except:
			pass 

		return redirect('action')

	else:
		question = QuizUser.get_new_questions()
		if question is not None:
			QuizUser.create_attempts(question)
		context = {
			'question': question,
		}

	return render(request, 'play/action.html', context)

def panel(request):
	total_user_quiz = QuizUsers.objects.order_by('-total_score')[:10]
	counter = total_user_quiz.count()

	context = {
		'users_quiz': total_user_quiz,
		'count_user': counter
	}

	return render(request, 'play/panel.html', context)

def loginView(request):
	title = 'HomeUser'
	form = UserLoginForm(request.POST or None)
	category=request.GET.get("name")
	category=Category.objects.filter(name=category)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		users = authenticate(username=username, password=password)
		login(request, users)
		return redirect('HomeUser')

	context = {
		'form':form,
		'title':title,
		
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

		'form':form,
		'title': title

	}

	return render(request, 'users/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')

