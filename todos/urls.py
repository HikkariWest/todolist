from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import *


urlpatterns = [
	path('', todo_list, name = "todo_list"),
	path('todo/<int:todo_id>/change_status/', change_todo_status, name = "change_todo_status"),
	path('todo_list/todo/<int:todo_id>/', todo_detail, name = "todo_detail"),
	path('categories/', category_list, name = "category_list"),
	path('todo_list/todo/create/', todo_create, name = "todo_create"),
	path('todo_list/todo/<int:todo_id>/edit/', todo_update, name = "todo_update"),
	path('todo_list/todo/delete/<int:todo_id>/', todo_delete, name = "todo_delete"),
	path('registration/', registration_page, name="registration_page"),
	path('profile/<int:user_id>/', profile_page, name="profile_page"),
	path('profile/<int:user_id>/change_status/', profile_change_status, name="profile_change_status"),
	path('buy_subs/', profile_change_status_page, name = 'profile_change_status_page'),
	path('login/', login_page, name='login_page'),
	path('profile/edit/', profile_edit_page, name='profile_edit'),
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='allauth/account/password_reset.html', html_email_template_name='allauth/account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt', form_class=MyPassResetForm), name = 'password_reset'),
	path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = "allauth/account/password_reset_done.html"), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'allauth/account/password_reset_confirm.html', form_class=MySetPassForm), name='password_reset_confirm'),
	path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'allauth/account/password_reset_complete.html'), name='password_reset_complete'),
	path('change_password/', change_password, name="change_password"),
	path('logout', logout_page, name="logout_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)