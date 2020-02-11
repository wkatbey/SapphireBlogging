from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'blog_admin'
urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
]
