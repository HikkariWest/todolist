from django.db import models
import os
from django.contrib.auth.models import Group, Permission, User


def user_image_dir(instance, filename):
	return os.path.join('avatars', f'{instance.user.id}', filename)


class Profile(models.Model):
	user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to=user_image_dir, blank=True, default='avatars/default.webp')
	first_name = models.CharField(max_length = 50)
	premium_status = models.BooleanField(default=False)
	last_name = models.CharField(max_length = 50)
	quantity_todos = models.IntegerField(default=0, null=True, blank=True)
	email = models.EmailField(max_length = 250, unique = True, null = True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.user.username


class Category(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name
		return f'{self.user.username}'


	class Meta:
		verbose_name='Категория'
		verbose_name_plural = 'Категории'



INTEREST_CHOICES = [
		('Low High', 'Не важно'),
		('High', 'Важно'),
		('Very High', 'Очень важно'),
	]

class Todo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	completed = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
	date_created = models.DateTimeField(auto_now=True)
	interest = models.CharField(default = 'Low High', choices=INTEREST_CHOICES, max_length = 15)

	def __str__(self):
		return self.name
		return f'{self.user.username}'

	class Meta:
		verbose_name='Задача'
		verbose_name_plural = 'Задачи'


	# def sub_check():
	# 	for user in Users:
	# 		if user.end_of_subscription_date == yesterday:
 #        		user.premium = False


# class UserPerm(models.Model):
# 	class Meta:
# 		permissions = [
# 			('common_user', 'Can add only 10 todos during all this time'),
# 			('premium_user', 'Can add infinite quantity todos during subscription'),
# 		]