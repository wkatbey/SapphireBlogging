from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'blog_admin'
urlpatterns = [
    path('', views.SphStyleBase.as_view(), name='dashboard'),
    path('api/GetAllCategories/', views.get_blog_categories),
    path('api/CreateCategory/', views.create_blog_category),
    path('api/GetCategoriesByTitle/<slug:title>', views.get_blog_category_by_title),
]
