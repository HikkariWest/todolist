from django.shortcuts import render
from .models import *

def todo_list(request):
	todos = Todo.objects.all()
	# categories = Category.objects.all()
	context = {'todos':todos}
	return render(request, 'todolist/todo_list.html', context)


def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)

def category(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'todolist/category_list.html')

