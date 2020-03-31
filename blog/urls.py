from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogEntryList.as_view(), name='blog-list'),
    path('create/<optional_param>', views.BlogEntryCreate.as_view(), name='new-entry'),
    path('update/<int:pk>/', views.BlogEntryUpdate.as_view(), name='update-entry'),
    path('delete/<int:pk>/', views.BlogEntryDelete.as_view(), name='delete-post'),
    path('view/<int:pk>/', views.BlogEntryDetail.as_view(), name='entry-detail'),
    path('user_posts/<int:pk>/', views.MyPosts.as_view(), name='user-entries'),
    path('category/<int:pk>/', views.BlogsByCategory.as_view(), name='entries-by-category')
]
