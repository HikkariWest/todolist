from django.shortcuts import render
from .models import *

def todo_list(request):
	todos = Todo.objects.all()
	context = {'todos':todos}
	return render(request, 'todolist/todo_list.html', context)


def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)
