from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from blog.models import Category
from rest_framework import status

@api_view(['GET'])
def get_blog_categories(request):
	serializer = CategorySerializer(Category.objects.all(), many=True)
	return Response(serializer.data)

@api_view(['GET'])
def get_blog_category_by_title(request, title):
	serializer = CategorySerializer(Category.objects.filter(title__contains=title), many=True)

	return Response(serializer.data)

@api_view(['POST'])
def create_blog_category(request):
	serializer = CategorySerializer(data=request.data)
	serializer.is_valid()

	serializer.save()

	return Response(serializer.data)


class Dashboard(View):
	template_name='blog_admin/index.html'

	def get(self, request):

		user = self.request.user
		context = {
			'user': user
		}

		if not user.is_authenticated or not user.is_staff:
			return HttpResponseRedirect(reverse_lazy('blog:blog-list'))

		return render(request, self.template_name, context)


class SphStyleBase(View):
	template_name='sph_style/base.html'

	def get(self, request):
		context = { }

		return render(request, self.template_name, context)

