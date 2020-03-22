from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Category",
        unique=True
    )

    description = models.CharField(
        max_length=500,
        verbose_name="Description"
    )

    slug = models.SlugField()

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.title]
        category = self.parent

        while category is not None:
            full_path.append(category.title)
            category = category.parent

        # For reference, makes a copy of the list in reverse order
        return ' -> '.join(full_path[::-1])

    def get_category_list(self):
        category = self
        breadcrumb = []

        while category is not None:
            breadcrumb.append(category)
            category = category.parent

        return breadcrumb[::-1]


class BlogEntry(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Title"
    )

    # primary_image = models.ImageField(verbose_name="Primary Image")
    text_entry = models.TextField()
    date_of_submission = models.DateTimeField()
    has_been_modified = models.BooleanField(default=False)
    date_updated = models.DateTimeField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    private = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[self.id])

    def get_category_list(self):
        category = self.category
        breadcrumb = []

        while category is not None:
            breadcrumb.append(category)
            category = category.parent

        return breadcrumb[::-1]
