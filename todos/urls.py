from django.urls import path
from .views import *


urlpatterns = [
	path('todo_list', todo_list, name = "todo_list"),
	path('todo_list/todo/<int:todo_id>/', todo_detail, name = "todo_detail"),
	path('categories/', category_list, name = "category_list"),
	path('todo_list/todo/create/', todo_create, name = "todo_create"),
	path('todo_list/todo/<int:todo_id>/edit/', todo_update, name = "todo_update"),
	path('categories/create', category_create, name="category_create"),
	path('profile/<int:user_id>/', profile_page, name="profile_page"),
	path('todo_list/todo/delete/<int:todo_id>', todo_delete, name = "todo_delete"),
]