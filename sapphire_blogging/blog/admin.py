from django.contrib import admin
from .models import Category, BlogEntry

admin.site.register(Category)
admin.site.register(BlogEntry)