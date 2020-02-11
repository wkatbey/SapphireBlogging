from django import forms
from django.forms import ModelForm
from blog.models import BlogEntry, Category
from datetime import datetime

class BlogEntryForm(ModelForm):
    class Meta:
        model = BlogEntry
        fields = (
            'title',
            #'primary_image',
            'category',
            'text_entry',
            'private'
        )

        widgets = {
            'category': forms.Select(
                attrs = {
                    'class': 'form-control'
                },
                choices = []
            ),
            'title': forms.TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'text_entry': forms.Textarea(
                attrs = {
                    'id': 'text-editor',
                    'class': 'form-control',
                    'rows': '17'
                }
            ),
            'private': forms.CheckboxInput(
                attrs = {
                    'id': 'make-post-private',
                    'class': 'custom-control-input'
                }
            )
        }

    def save(self, commit=True):
        blog_instance = super(BlogEntryForm, self).save(commit=False)
        blog_instance.date_of_submission = datetime.now()
        blog_instance.date_updated = datetime.now()

        return blog_instance
