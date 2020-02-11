from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogEntryList.as_view(), name='blog-list'),
    path('create/<optional_param>', views.BlogEntryCreate.as_view(), name='blog-create'),
    path('update/<int:pk>/', views.BlogEntryUpdate.as_view(), name='blog-update'),
    path('delete/<int:pk>/', views.BlogEntryDelete.as_view(), name='blog-delete'),
    path('view/<int:pk>/', views.BlogEntryDetail.as_view(), name='blog-detail'),
    path('user_posts/<int:pk>/', views.MyPosts.as_view(), name='user-posts'),
    path('category/<int:pk>/', views.BlogsByCategory.as_view(), name='blogs-by-category')
]
