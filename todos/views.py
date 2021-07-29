from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from .decorators import unauthanticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_page')
def change_todo_status(request, todo_id):
	todo = get_object_or_404(Todo, id = todo_id)
	if todo.user != request.user:
		return redirect('todo_list')
	todo.completed = not todo.completed
	todo.save()
	return redirect('todo_list')


@login_required(login_url='login_page')
def todo_list(request):
	categories = Category.objects.all()
	todos = Todo.objects.filter(user=request.user)
	context = {'todos':todos, 'categories':categories}
	return render(request, 'todolist/todo_list.html', context)

@login_required(login_url='login_page')
def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	if todo.user != request.user:
		return redirect('todo_list')
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)


@login_required(login_url='login_page')
def todo_create(request):
	todos = Todo.objects.values('interest')
	categories = Category.objects.all()
	profile = request.user.profile
	form = TodoCreateForm()
	if request.method == "POST":
		form = TodoCreateForm(request.POST)
		if form.is_valid():
			if profile.quantity_todos < 10 or profile.premium_status == True:
				todo = form.save(commit = False)
				todo.user=request.user
				todo.save()
				profile.quantity_todos += 1
				profile.save()
				return redirect('todo_list')
			elif profile.quantity_todos >= 10 and profile.premium_status == False:
				return redirect("profile_change_status_page")
	context = {'form':form, 'todos':todos, 'categories':categories}
	return render(request, 'todolist/todo_create.html', context)



@login_required(login_url='login_page')
def todo_update(request, todo_id):
	categories = Category.objects.all()
	todo = get_object_or_404(Todo, id = todo_id)
	if todo.user != request.user:
		return redirect('todo_list')
	form = TodoUpdateForm(instance=todo)
	if request.method == "POST" and todo.user == request.user:
		form = TodoUpdateForm(request.POST, instance = todo)
		if form.is_valid():
			form.save()
			return redirect('todo_list')
	context = {'form':form, 'categories':categories}
	return render(request, 'todolist/todo_update.html', context)



@login_required(login_url='login_page')
def category_list(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'todolist/category_list.html', context)


@login_required(login_url='login_page')
def todo_delete(request, todo_id):
	todo = get_object_or_404(Todo, id = todo_id)
	if todo.user != request.user:
		return redirect('todo_list')
	if request.method == 'POST':
		todo.delete()
		return redirect('todo_list')
	return render(request, 'todolist/todo_delete.html')


#Профили, регистрация и авторизация


@login_required(login_url='login_page')
def profile_page(request, user_id):
	user = Profile.objects.get(id = user_id)
	context = {'user':user}
	return render(request, 'account/profile_page.html', context)

@unauthanticated_user
def registration_page(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = True
			user.save()
			return redirect("login_page")
	context = {'form': form}
	return render(request, 'account/registration_page.html', context)


@login_required(login_url='login_page')
def profile_change_status_page(request):
	return render(request, 'account/buy_subscription.html')


@login_required(login_url='login_page')
def profile_change_status(request, user_id):
	user = Profile.objects.get(id=user_id)
	profile = request.user.profile
	if request.method == "POST":
		if profile.premium_status == False:
			profile.premium_status = True
			profile.save()
		else:
			return HttpResponse("У вас уже есть премиум статус")
	return redirect("todo_list")
	return render(render, 'account/buy_subscription.html')


@unauthanticated_user
def login_page(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username = cd['username'], password = cd['password'])
			if user is not None:
				login(request, user)
				return redirect('todo_list')
	context = {'form': form}
	return render(request, 'account/login_page.html', context)


@login_required(login_url='login_page')
def profile_edit_page(request):
	u_form = UserEditForm(instance=request.user)
	p_form = ProfileEditForm(instance=request.user.profile)
	if request.method == 'POST':
		p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
		u_form = UserEditForm(request.POST, instance=request.user)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('todo_list')
	context = {'u_form':u_form, 'p_form':p_form}
	return render(request, 'account/profile_edit.html', context)


@login_required(login_url='login_page')
def logout_page(request):
	logout(request)
	return redirect('login_page')


@login_required(login_url='login_page')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Ваш пароль был успешно изменен!', extra_tags='safe')
			return redirect('change_password')
		else:
			messages.error(request, 'Пожалуйста, исправьте ошибку ниже.', extra_tags='safe')
	else:
		form = PasswordChangeForm(request.user)
	context = {'form':form}
	return render(request, 'account/change_password.html', context)