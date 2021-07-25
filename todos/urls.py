from django.urls import path
from .views import *


urlpatterns = [
	path('todo_list', todo_list, name = "todo_list"),
	path('todo/<int:todo_id>/change_status', change_todo_status, name = "change_todo_status"),
	path('todo_list/todo/<int:todo_id>/', todo_detail, name = "todo_detail"),
	path('categories/', category_list, name = "category_list"),
	path('categories/create', category_create, name="category_create"),
	path('todo_list/todo/create/', todo_create, name = "todo_create"),
	path('todo_list/todo/<int:todo_id>/edit/', todo_update, name = "todo_update"),
	path('todo_list/todo/delete/<int:todo_id>', todo_delete, name = "todo_delete"),
	path('registration/', registration_page, name="registration_page"),
	path('profile/<int:user_id>/', profile_page, name="profile_page"),
	path('profile/<int:user_id>/change_status/', profile_change_status, name="profile_change_status"),
	path('buy_subs/', profile_change_status_page, name = 'profile_change_status_page')
]