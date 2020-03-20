from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from blog.models import Category
from rest_framework import serializers


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
	try:

		serializer.is_valid(raise_exception=True)

		serializer.save()

		return Response(serializer.data)
	except (serializers.ValidationError, KeyError, ValueError) as e:
		context = {'error': str(e)}
		return Response(status=400, data=context)


@api_view(['PUT'])
def update_blog_category(request):
    print("does this exist?", request.data['id'])
    category = Category.objects.get(pk=request.data['id'])
    serializer = CategorySerializer(category, data=request.data)
    
    try:

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
    except (serializers.ValidationError, KeyError, ValueError) as e:
        context = {'error': str(e)}
        return Response(status=400, data=context)


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

