from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import TodoForm

def todo_list(request):
	todos = Todo.objects.all()
	# categories = Category.objects.all()
	context = {'todos':todos}
	return render(request, 'todolist/todo_list.html', context)

def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)

def todo_update(request, todo_id):
	categories = Category.objects.all()
	category = request.POST.get('category_select')
	todo = get_object_or_404(Todo, id = todo_id)
	form = TodoForm(request.POST or None, instance = todo)
	if request.method == "POST":
		form = TodoForm(request.POST, instance = todo)
		if form.is_valid():
			form.save()
			return redirect('todo_list/todo/'+id)
	context = {'form':form, 'categories':categories}
	return render(request, 'todolist/todo_update.html', context)


def category_list(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'todolist/category_list.html', context)

