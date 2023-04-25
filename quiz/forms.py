from django import forms
from .models import  Question, ChooseAnswer, QuestionsAnswered
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, get_user_model


User = get_user_model()

class ChooseInlineFormset(forms.BaseInlineFormSet):
	def clean(self):
		super(ChooseInlineFormset, self).clean()

		correct_answer = 0
		for form in self.forms:
			if not form.is_valid():
				return

			if form.cleaned_data and form.cleaned_data.get('correct') is True:
				correct_answer += 1

		try:
			assert correct_answer == Question.NUMBER_OF_RESPONSES_ALLOWED
		except AssertionError:
			raise forms.ValidationError('Exactly one answer is allowed')


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This user is not active")

		return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User 

		fields = [

			'first_name',
			'last_name',
			'username',
			'email',
			'password1',
			'password2'

		]