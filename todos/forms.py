from django import forms
from .models import *


class TodoUpdateForm(forms.ModelForm):
	completed = forms.BooleanField(widget= forms.CheckboxInput)
	class Meta:
		model = Todo
		fields = [
			"name",
			"description",
			# "completed",
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



# class CreateUserForm(UserCreationForm):
# 	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
# 	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
# 	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
# 	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)