from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='')),
    path('user-list/', views.UserList.as_view(), name='user-list'),
    path('user-profile/', views.UserList.as_view(), name='user-profile'),
]
