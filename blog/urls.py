from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.Portal.as_view(), name='blog-list'),
    path('create', views.CreateEntry.as_view(), name='new-entry'),
    path('update/<int:pk>/', views.UpdateEntry.as_view(), name='update-entry'),
    path('delete/<int:pk>/', views.DeleteEntry.as_view(), name='delete-post'),
    path('view/<int:pk>/', views.EntryDetail.as_view(), name='entry-detail'),
    path('user_posts/<int:pk>/', views.MyPosts.as_view(), name='user-entries'),
    path('category/<int:pk>/', views.PostsByCategory.as_view(), name='entries-by-category')
]
