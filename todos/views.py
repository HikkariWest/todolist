from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .filters import TodoFilter
from .forms import *
# from search_views.search import SearchListView
# from search_views.filters import BaseFilter

# def is_valid_queryparam(param):
# 	return param != '' and param is not None

def todo_list(request):
	todos = Todo.objects.all()
	# myFilter = TodoFilter(request.GET, queryset=todos)
	# todos = myFilter.qs
	# todos_filtered = TodoFilter(request.GET, queryset=todos)

	context = {'todos':todos}
	return render(request, 'todolist/todo_list.html', context)

def todo_detail(request, todo_id):
	todo = Todo.objects.get(id = todo_id)
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)

def todo_create(request):
	todos = Todo.objects.all()
	categories = Category.objects.all()
	form = TodoCreateForm()
	if request.method == "POST":
		form = TodoCreateForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
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
			form.save()
			return redirect('todo_list')
	context = {'form':form, 'categories':categories}
	return render(request, 'todolist/todo_update.html', context)


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
	form = CategoryCreateForm(instance = request.user)
	if request.method == "POST":
		form = CategoryCreateForm(request.POST, instance = request.user)
		if form.is_valid():
			form.save()
			return redirect("category_list")
	context = {'form':form}
	return render(request, 'todolist/category_create.html', context)


def profile_page(request, user_id):
	user = User.objects.get(id = user_id)
	context = {'user':user}
	return render(request, 'account/profile_page.html', context)



# class TodoFilter(BaseFilter):
# 	search_fields = {
# 		'search_text' : ['name', 'description'],
# 		'search_date_exact' : { 'operator' : '__exact', 'fields' : ['date_created'] },
#     }

# class ActorsSearchList(SearchListView):
# 	model = Todo
# 	paginate_by = 30
# 	template_name = "base.html"
# 	form_class = TodoSearchForm
# 	filter_class = TodoFilter


# def todo_search(request):
# 	search = request.GET.get('search','')
# 	if search:
# 		todos = Todo.objects.filter(
# 			Q(name__icontains = search)
# 				|
# 			Q(description__icontains = search))
# 		serialized_todo = serializers.serialize('json', todos, fields = ('name'))
# 		return JsonResponse({'todos':serialized_todo})
# 	else:
# 		todos = Todo.objects.all()
# 	context = {'todos':todos, 'search':search}
# 	return render(request, '', context)
