from django import forms
from .models import InitiativeJoin, Motivation

class InitiativeJoinForm(forms.ModelForm):
	motivation = forms.ModelMultipleChoiceField(
		queryset=Motivation.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False,
		label='Motivation/Why do you want to join?',
	)

	class Meta:
		model = InitiativeJoin
		fields = '__all__'
