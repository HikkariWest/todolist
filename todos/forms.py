from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login


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

#Профили

class CreateUserForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Введите пароль'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Повторите пароль'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Введите свою почту'}))

	class Meta:
		model = User
		fields = ['username', 'first_name','last_name', 'password1', 'password2', 'email']




class LoginForm(AuthenticationForm):
	username = forms.CharField(widget = forms.TextInput(attrs = {
		'placeholder': 'Логин', 'class':'form-control'
		}), required=True)
	password = forms.CharField(widget = forms.PasswordInput(attrs = {
		'placeholder': 'Пароль', 'class':'form-control'
		}), required=True)



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
	photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'custom-file-input', 'type':'file', 'id':'customFile'}))
	class Meta:
		model = Profile
		fields = ['photo']


class BootstrapStylesMixin:
	field_names = None


class MyPassResetForm(BootstrapStylesMixin, PasswordResetForm):
	field_names = ['email']

	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)

	    if self.field_names:
	    	for fieldname in self.field_names:
	    		self.fields[fieldname].widget.attrs = {'class':'form-control', 'style':'width:800px; margin-left:100px'}
	    else:
	    	raise ValueError('The field_names must be set')

class MySetPassForm(BootstrapStylesMixin, SetPasswordForm):
	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)

	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'style':'width:750px; height:55px; margin-left:250px; margin-top:60px', 'placeholder':'Введите пароль'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'style':'width:750px; height:55px; margin-left:250px; margin-top:60px', 'placeholder':'Повторите пароль'}))

	labels = {
            'new_password1': 'Пароль',
            'new_password2': 'Повторите пароль',
        }
