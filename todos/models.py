from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name='Категория'
		verbose_name_plural = 'Категории'


class Todo(models.Model):
	INTEREST_CHOICES = [
    	('Low', 'Не важно'),
    	('High', 'Важно'),
   		('Very High', 'Очень важно'),
	]
	# INTEREST_CHOICES = (
	# 	(1, ('Не важно')),
	# 	(2, ('Важно')),
	# 	(3, ('Очень важно')),
	# 	)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	completed = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
	date_created = models.DateTimeField(auto_now=True)
	interest = models.CharField(default = 1, choices=INTEREST_CHOICES, max_length = 15)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name='Задача'
		verbose_name_plural = 'Задачи'

