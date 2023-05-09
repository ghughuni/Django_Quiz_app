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
	category=models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=False)
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
    users = models.ForeignKey(User, on_delete=models.CASCADE, default=False, null=False)
    total_score = models.DecimalField(verbose_name='total_score', default=0, decimal_places=2, max_digits=10)
    choose_category = models.DecimalField(verbose_name='choose_category', default=0, decimal_places=0, max_digits=10)
     
    # def create_attempts(self, question, choose_category, selected_answer, is_correct):
    #     question_answered = QuestionsAnswered(
    #         quizUser=self,
    #         question=question,
    #         category=choose_category,
    #         selected_answer=selected_answer,
    #         correct=is_correct
    #     )
    #     question_answered.save()

    # def validate_attempts(self, question_answered, selected_answer):
    #     if question_answered.question_id != selected_answer.question_id:
    #         return

    #     question_answered.selected_answer = selected_answer
    #     if selected_answer.correct is True:
    #         question_answered.correct = True
    #         question_answered.obtained_score = selected_answer.question.max_score
    #         question_answered.answer = selected_answer
    #     else:
    #         question_answered.answer = selected_answer

    #     question_answered.save()

    #     self.update_score()

    # def update_score(self):
    #     updated_score = self.filter(correct=True).aggregate(
    #         models.Sum('obtained_score'))['obtained_score__sum']

    #     self.total_score = updated_score
    #     self.save()

class QuestionsAnswered(models.Model):
    quizUser = models.ForeignKey(QuizUsers, on_delete=models.CASCADE, related_name='attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    category = models.IntegerField()
    answer = models.ForeignKey(ChooseAnswer, on_delete=models.CASCADE, null=True)
    correct  = models.BooleanField(verbose_name='Is this the correct answer?', default=False, null=False)
    obtained_score = models.DecimalField(verbose_name='Obtained Score', default=0, decimal_places=2, max_digits=6)
