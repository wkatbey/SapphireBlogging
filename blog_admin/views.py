from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class Dashboard(View, LoginRequiredMixin):
	template_name='blog_admin/index.html'

	def get(self, request):

		user = self.request.user
		context = {
			'user': user
		}

		if not user.is_authenticated or not user.is_staff:
			return HttpResponseRedirect(reverse_lazy('blog:blog-list'))

		return render(request, self.template_name, context)