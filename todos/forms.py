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

class CategoryCreateForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = [
			'name',
			'description',
			]


# class TodoSearchForm(forms.Form):
#     search_text =  forms.CharField(
#                     required = False,
#                     label='Search todo name or todo description!',
#                     widget=forms.TextInput(attrs={'placeholder': 'search here!'})
#                   )

#     search_date_exact = forms.DateTimeField(
#                     required = False,
#                     label='Search date (exact match)!'
#                   )
