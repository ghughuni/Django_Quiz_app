from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import random

class Category(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name 
	
class Question(models.Model):
	NUMBER_OF_RESPONSES_ALLOWED = 1
	text = models.TextField(verbose_name='Text of Question')
	max_score = models.DecimalField(verbose_name='Max score', default=3, decimal_places=2, max_digits=6)
	category=models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
	def __str__(self):
		return self.text 


class ChooseAnswer(models.Model):
	MAX_RESPONSES = 4
	question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
	correct = models.BooleanField(verbose_name='Is this the question correct?', default=False, null=False)
	text = models.TextField(verbose_name='Text of responses')
	def __str__(self):
		return self.text

class QuizUsers(models.Model):
	users = models.OneToOneField(User, on_delete=models.CASCADE)
	total_score = models.DecimalField(verbose_name='total_score', default=0, decimal_places=2, max_digits=10)

	def create_attempts(self, question):
		attempt = QuestionsAnswered(question=question, quizUser=self)
		attempt.save()

	def get_new_questions(self):
		answered = QuestionsAnswered.objects.filter(quizUser=self).values_list('question__pk', flat=True)
		remaining_questions = Question.objects.exclude(pk__in=answered)
		if not remaining_questions.exists():
			return None
		return random.choice(remaining_questions)

	def validate_attempts(self, question_answered, selected_answer):
		if question_answered.question_id != selected_answer.question_id:
			return

		question_answered.selected_answer = selected_answer
		if selected_answer.correct is True:
			question_answered.correct = True
			question_answered.obtained_score = selected_answer.question.max_score
			question_answered.answer = selected_answer
		else:
			question_answered.answer = selected_answer

		question_answered.save()

		self.update_score()

	def update_score(self):
		updated_score = self.attempts.filter(correct=True).aggregate(
			models.Sum('obtained_score'))['obtained_score__sum']

		self.total_score = updated_score
		self.save()

class QuestionsAnswered(models.Model):
	quizUser = models.ForeignKey(QuizUsers, on_delete=models.CASCADE, related_name='attempts')
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(ChooseAnswer, on_delete=models.CASCADE, null=True)
	correct  = models.BooleanField(verbose_name='Is this the correct answer?', default=False, null=False)
	obtained_score = models.DecimalField(verbose_name='Obtained Score', default=0, decimal_places=2, max_digits=6)
