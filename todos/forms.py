from django import forms
from .models import *


class TodoUpdateForm(forms.ModelForm):
	class Meta:
		model = Todo
		fields = [
			"name",
			"description",
			"completed",
			"category",
			"interest",
		]

class TodoCreateForm(forms.ModelForm):
	class Meta:
		model = Todo
		fields = [
			"name",
			"description",
			"category",
			"interest",
		]