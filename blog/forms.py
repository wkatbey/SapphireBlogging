from django import forms


class EntryForm(forms.Form):
	category_title = forms.CharField()
	title = forms.CharField()

	text_entry = forms.CharField()

	private = forms.BooleanField()

	def create():
		pass

	def update():
		pass