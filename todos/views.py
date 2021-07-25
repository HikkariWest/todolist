from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .filters import TodoFilter
from django.http import JsonResponse, HttpResponse
from .forms import *
from django.views import View
from django.urls import reverse
from .decorators import unauthanticated_user
# from search_views.search import SearchListView
# from search_views.filters import BaseFilter

# def is_valid_queryparam(param):
# 	return param != '' and param is not None

def todo_list(request):
	categories = Category.objects.all()
	category_name = request.POST.get('search')
	if category_name:
		todos = Todo.objects.all().filter(category__name__contains="category")
	else:
		todos = Todo.objects.all()
	# print(filtered_todos)
	context = {'todos':todos, 'categories':categories}
	return render(request, 'todolist/todo_list2.html', context)

def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	if request.method == "POST":
		todo = get_object_or_404(Todo, id=request.POST['todo_id'])
		todo.completed = not todo.completed
		todo.save()
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)

def todo_create(request):
	quantity_todos = Profile.objects.all().values("quantity_todos")
	todos = Todo.objects.all()
	categories = Category.objects.all()
	profile = request.user.profile
	form = TodoCreateForm()
	if request.method == "POST":
		form = TodoCreateForm(request.POST)
		print(form)
		if form.is_valid():
			if request.user.profile.quantity_todos < 10 and request.user.profile.premium_status == False:
				todo = form.save(commit = False)
				todo.user=request.user
				todo.save()
				# profile = request.user.profile
				profile.quantity_todos += 1
				profile.save()
				return redirect('todo_list')
			elif request.user.profile.quantity_todos == 10 and request.user.profile.premium_status == False:
				return HttpResponse("Вы уже добавили 10 задач, купите премиум и можете добавлять сколько захотите")
			elif request.user.profile.premium_status == True:
				todo = form.save(commit = False)
				todo.user=request.user
				todo.save()
				profile.quantity_todos += 1
				profile.save()
				return redirect('todo_list')
	context = {'form':form, 'todos':todos, 'categories':categories}
	return render(request, 'todolist/todo_create.html', context)


def todo_update(request, todo_id):
	categories = Category.objects.all()
	category = request.POST.get('category_select')
	todo = get_object_or_404(Todo, id = todo_id)
	form = TodoUpdateForm(request.POST, instance = todo)
	if request.method == "POST":
		form = TodoUpdateForm(request.POST, instance = todo)
		if form.is_valid():
			todo.save()
			return redirect('todo_list')
	context = {'form':form, 'categories':categories}
	return render(request, 'todolist/todo_update.html', context)


def change_todo_status(request, todo_id):
	todo = get_object_or_404(Todo, id = todo_id)
	todo.completed = not todo.completed
	todo.save()
	return redirect('todo_list')


def category_list(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'todolist/category_list.html', context)

def todo_search(request):
	search_request = request.GET.get('q')
	if search_request:
		print(search_request)
		todos = Todo.objects.filter(name__istartswith = search_request)
		todos2 = Todo.objects.filter(description__istartswith = search_request)
		context = {'todos':todos, 'todos2':todos2}
	else:
		todos = Todo.objects.all()
	context = {'todos':todos}
	return render(request, 'todolist/todo_list.html', context)

def category_create(request):
	form = CategoryCreateForm()
	print(request.user)
	if request.method == "POST":
		form = CategoryCreateForm(request.POST)
		if form.is_valid():
			if request.user.profile.premium_status == True:
				category = form.save(commit=False)
				category.user=request.user
				category.save()
				return redirect("category_list")
			elif request.user.profile.premium_status == False:
				return HttpResponse("Извините, но у вас нет прав добавлять категории, купите премиум статус и можете добавлять категории")
	context = {'form':form}
	return render(request, 'todolist/category_create.html', context)


def profile_page(request, user_id):
	user = Profile.objects.get(id = user_id)
	context = {'user':user}
	return render(request, 'account/profile_page.html', context)


def todo_delete(request, todo_id):
	todo = get_object_or_404(Todo, id = todo_id)
	if request.method == 'POST':
		todo.delete()
	context = {'todo':todo}
	return render(request, 'todolist/todo_delete.html', context)


#Профили, регистрация и авторизация


@unauthanticated_user
def registration_page(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			name = user.username
			user.save()
			return redirect("accounts/login")
	context = {'form': form}
	return render(request, 'account/registration_page.html', context)

def profile_change_status_page(request):
	return render(request, 'account/buy_subscription.html')

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
