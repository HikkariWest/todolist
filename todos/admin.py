from django.contrib import admin
from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
	list_display = ['name', 'completed', 'interest', 'category']
	list_editable = ['completed', 'interest']
	list_filter = ['completed', 'interest']
	search_fields = ['name', 'category__name']
	save_as = True