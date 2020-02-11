from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('user.urls')),
    path('blog-admin/', include('blog_admin.urls')),
]
