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


@login_required(login_url='login_page') #Декоратор, который перенаправляет на страницу логина, если пользователь не зарегистрирован
def change_todo_status(request, todo_id): #Функция смены статуса задачи
	todo = get_object_or_404(Todo, id = todo_id) #Достаем задачу из базы данных
	if todo.user != request.user: #Проверяем принадлежит ли задача авторизованному пользователю
		return redirect(todo_list) #Переадресация на список задач
	todo.completed = not todo.completed #Сама смена статуса
	todo.save() #Сохранение задачи в базе данных(точнее изменений в базе данных)
	return redirect(todo_list) #После изменения пересылает нас на страницу списка задач


@login_required(login_url='login_page')
def todo_list(request): #Функция списка задач
	categories = Category.objects.all() #Достаем все категории из базы данных
	todos = Todo.objects.filter(user=request.user) #Достаем все задачи из базы данных, которые принадлежат авторизованному юзеру
	context = {'todos':todos, 'categories':categories}
	return render(request, 'todolist/todo_list.html', context)

@login_required(login_url='login_page')
def todo_detail(request, todo_id): #Функция подробностей задачи
	todo = Todo.objects.get(id = todo_id) #Достаем определенную задачу по айди
	if todo.user != request.user: #Проверяем принадлежит ли задача авторизованному пользователю
		return redirect(todo_list) #Переадресация на список задач
	context = {'todo':todo}
	return render(request, 'todolist/todo_detail.html', context)


@login_required(login_url='login_page')
def todo_create(request): #Функция создания задачи
	profile = request.user.profile #Создаем переменную, которую, ниже в этой функции, будем использовать чтобы сократить несколько букв
	form = TodoCreateForm() #Определяем форму
	if request.method == "POST": #Проверка на метод POST
		form = TodoCreateForm(request.POST) #Вносим этот запрос в форму
		if form.is_valid(): #Проверяем форму на валидность
			if profile.quantity_todos < 10 or profile.premium_status == True: #Проверяем на количество задач у пользователя и наличие премиум статуса
				todo = form.save(commit = False) #Делаем переменную в которой хранится сохранение формы
				todo.user=request.user #Присваиваем созданную задачу пользователю
				todo.save() #Сохраняем задачу
				profile.quantity_todos += 1 #Увеличиваем количество задач у пользователя после сохранения задачи
				profile.save() #Сохраняем нынешнее количество задач в базе данных
				return redirect(todo_list) #Переход на страницу списка задач
			elif profile.quantity_todos >= 10 and profile.premium_status == False: #Противоположная проверка, что если у пользователя больше задач, чем 10 и нет премиум статуса, то создавать задачи он не может
				return redirect("profile_change_status_page") #Переход на страницу покупки премиум статуса
	context = {'form':form}
	return render(request, 'todolist/todo_create.html', context)



@login_required(login_url='login_page')
def todo_update(request, todo_id): #Функция редактирования задач
	todo = get_object_or_404(Todo, id = todo_id) #Достаем задачу по айди, которую будем редактировать
	if todo.user != request.user: #Проверяем принадлежит ли задача авторизованному пользователю
		return redirect(todo_list) #Переадресация на список задач
	form = TodoUpdateForm(instance=todo) #Определяем форму с уже готовой задачей
	if request.method == "POST": #Проверяем на метод POST
		form = TodoUpdateForm(request.POST, instance = todo) #Теперь заносим запрос формы в форму
		if form.is_valid(): #Проверяем форму на валидность
			form.save() #Сохраняем форму
			return redirect(todo_list) #Переходим на страницу списка задач
	context = {'form':form}
	return render(request, 'todolist/todo_update.html', context)



@login_required(login_url='login_page')
def category_list(request): #Функция списка категорий
	categories = Category.objects.all() #Достаем все категории из базы данных
	context = {'categories':categories}
	return render(request, 'todolist/category_list.html', context)


@login_required(login_url='login_page')
def todo_delete(request, todo_id): #Функция удаления задачи
	todo = get_object_or_404(Todo, id = todo_id) #Достаем задачу по айди 
	if todo.user != request.user: #Проверяем принадлежит ли задача авторизованному пользователю
		return redirect(todo_list) #Переадресация на список задач
	if request.method == 'POST': #Проверка на метод POST 
		todo.delete() #Удаляем задачу
		return redirect(todo_list)
	return render(request, 'todolist/todo_delete.html')


#Профили, регистрация и авторизация


@login_required(login_url='login_page')
def profile_page(request, user_id): #Функция страницы профиля
	user = Profile.objects.get(id = user_id) #Достаем профиля из базы данных
	profile = request.user.profile #Создаем переменную, которую, ниже в этой функции
	if user != profile: #Проверяем на свой ли профиль перешел пользователь, если нет,
		return redirect(todo_list) #то перенаправляем его на страницу списка задач
	context = {'user':user}
	return render(request, 'account/profile_page.html', context)


@unauthanticated_user
def login_page(request): #Функция авторизации пользователей
	form = LoginForm() #Определяем форму, которой будем пользоваться
	if request.method == 'POST': #Проверка на метод POST
		form = LoginForm(data=request.POST) #Заносим переменную data в форму
		if form.is_valid(): #Проверяем форму на валидность
			cd = form.cleaned_data #Делаем переменную и форму в ней
			user = authenticate(username = cd['username'], password = cd['password']) #Делаем переменную с аутентификацией(авторизацией)
			if user is not None: #Проверяем на наличие пользователя в базе данных
				login(request, user) #Логинимся данными, которые ввели в форме
				return redirect(todo_list) #Переходим на страницу списка задач
	context = {'form': form}
	return render(request, 'account/login_page.html', context)


@unauthanticated_user
def registration_page(request): #Функция регистрации аккаунта
	form = CreateUserForm() #Определяем форму, которую будем использовать
	if request.method == 'POST': #Проверка на метод POST
		form = CreateUserForm(request.POST) #Заносим метод POST в форму
		if form.is_valid(): #Проверяем форму на валидность
			user = form.save(commit=False) #Создаем переменную в которой лежит сохранение формы
			user.is_active = True #Присваиваем созданному пользователю статус Active
			user.save() #Сохраняем пользователя
			return redirect("login_page") #Переходим на страницу логина
	context = {'form': form}
	return render(request, 'account/registration_page.html', context)


@login_required(login_url='login_page')
def profile_change_status_page(request): #Функция чисто ради страницы для смены премиум статуса у пользователя
	return render(request, 'account/buy_subscription.html')


@login_required(login_url='login_page')
def profile_change_status(request, user_id): #Функция для смены премиум статуса у пользователя
	user = Profile.objects.get(id=user_id) #Выбираем пользователя, который поменяет свой статус
	profile = request.user.profile #Переменная в который хранится нынешний юзер
	if user != profile: #Проверяем на свой ли профиль перешел пользователь, если нет,
		return redirect(todo_list) #то перенаправляем его на страницу списка задач
	if request.method == "POST": #Проверка на метод POST
		if profile.premium_status == False: #Проверка профиля на наличие премиум статуса
			profile.premium_status = True #Задачем профилю премиум статус
			profile.save() #Сохраняем изменения с базе данных
		else:
			return HttpResponse("У вас уже есть премиум статус") #Перенаправляем юзера на сообщение о наличии премиум статуса
	return redirect("todo_list") #Переходим на страницу списка задач
	return render(render, 'account/buy_subscription.html')




@login_required(login_url='login_page')
def profile_edit_page(request): #Функция редактирования профиля
	u_form = UserEditForm(instance=request.user) #Определяем форму измениня стандартных данных юзера
	p_form = ProfileEditForm(instance=request.user.profile) #Определяем форму изменения данных профиля модели Profile
	if request.method == 'POST': #Проверка на метод POST
		u_form = UserEditForm(request.POST, instance=request.user) #Заносим в форму изменения стандартного юзера запрос POST
		p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile) #Заносим в форму изменения профиля модели Profile запрос POST и файл в виде аватарки профиля(request.FILES)
		if u_form.is_valid() and p_form.is_valid(): #Проверка обеих форм на валидность
			u_form.save() #Сохранения формы стандартного юзера
			p_form.save() #Сохранения формы профиля
			return redirect(todo_list) #Переходим на страницу списка задач
	context = {'u_form':u_form, 'p_form':p_form}
	return render(request, 'account/profile_edit.html', context)


@login_required(login_url='login_page')
def logout_page(request): #Функция логаута
	logout(request) #Происходит сам логаут юзера
	return redirect('login_page') #Переход на страницу логина

@login_required(login_url='login_page')
def change_password(request): #Функция смены пароля
	if request.method == 'POST': #Проверка на метод POST
		form = PasswordChangeForm(request.user, request.POST) #Определяем форму и заносим туда запрос POST
		if form.is_valid(): #Проверка формы на валидность
			user = form.save() #Создаем переменную, в которой лежит сохранение формы
			update_session_auth_hash(request, user)  #Сама функция, которая меняет пароль
			messages.success(request, 'Ваш пароль был успешно изменен!', extra_tags='safe') #Сообщение об успешной смене пароля
			return redirect('change_password') #Переход на страницу смены пароля, чтобы вывелось сообщение
		else:
			messages.error(request, 'Пожалуйста, исправьте ошибку ниже.', extra_tags='safe') #Сообщение о том, что пользователь допустил ошибку в паролях
	else:
		form = PasswordChangeForm(request.user) #Форма без запроса POST
	context = {'form':form}
	return render(request, 'account/change_password.html', context)