from django.contrib import admin
from .models import Question, ChooseAnswer, QuestionsAnswered, QuizUsers, Category
from .forms import ChooseInlineFormset

class ChooseAnswerline(admin.TabularInline):
	model = ChooseAnswer
	can_delete =False
	max_num = ChooseAnswer.MAX_RESPONSES
	min_num = ChooseAnswer.MAX_RESPONSES
	formset = ChooseInlineFormset
	category_fields = ['name']


class QuestionAdmin(admin.ModelAdmin):
	model = Question
	inlines = (ChooseAnswerline, )
	list_display = ['text',]
	search_fields = ['text', 'questions__text']


class QuestionsAnsweredAdmin(admin.ModelAdmin):
	list_display = ['question', 'answer', 'correct', 'obtained_score']

	class Meta:
		model = QuestionsAnswered

admin.site.register(Question, QuestionAdmin)
admin.site.register(ChooseAnswer)
admin.site.register(Category)
admin.site.register(QuizUsers)
admin.site.register(QuestionsAnswered)
