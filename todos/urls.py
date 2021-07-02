from django.urls import path
from .views import *


urlpatterns = [
	path('', todo_list, name = "todo_list"),
	path('todo_list/todo/<int:todo_id>/', todo_detail, name = "todo_detail"),
	path('categories/', category_list, name = "category_list")
]