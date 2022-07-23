from django.forms import forms
from .models import BlogEntry, Category
from django.contrib.auth.models import User

class BlogEntryForm(forms.Form):
	date_of_submission = forms.DateTimeField()
	date_updated = forms.DateTimeField()

	has_been_modified = forms.BooleanField()

	author = forms.ModelChoiceField(queryset=User.objects.all())
	title = forms.CharField()

	text_entry = forms.CharField()

	private = forms.BooleanField()

	category = forms.ModelChoiceField(queryset=Category.objects.all())

	class Meta:
		model = BlogEntry
		fields = ['date_of_submission', 'date_updated', 'has_been_modified', 'author', 'title', 'text_entry', 'private', 'category']