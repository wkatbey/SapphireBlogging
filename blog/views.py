from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from blog.forms import BlogEntryForm
from blog.models import BlogEntry, Category
from .category_traversal import get_blogs_by_category
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from operator import attrgetter

'''
class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = ''
'''

class BlogsByCategory(View):
    template_name = 'blog/blogentry_list_category.html'

    def get(self, request, pk):
        category_id = pk

        categories = Category.objects.all()
        category = Category.objects.get(pk=category_id)

        blogs = get_blogs_by_category(category) 
        
        breadcrumbs = category.get_category_list()
        breadcrumbs_max = len(breadcrumbs)-1

        breadcrumbs = enumerate(breadcrumbs)
    
        context = {
            'blogs': blogs,
            'breadcrumbs': breadcrumbs,
            'breadcrumbs_max': breadcrumbs_max,
            'category': category
        }

        return render(request, self.template_name, context)

class BlogEntryList(ListView):
    model = BlogEntry
    context_object_name = 'blog_entries'
    
    # In case we need to define new dictionary elements
    # in the context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_entries = list(context['blog_entries'])

        blog_entries = sorted(blog_entries, key=attrgetter('date_of_submission'))

        # Filtering out private entries
        blog_entries = list(filter(lambda entry: not entry.private, blog_entries))

        blog_entries.reverse()

        context['blog_entries'] = blog_entries
        return context

class BlogEntryDetail(DetailView):
    model = BlogEntry
    context_object_name = 'blog_entry'


    def get(self, request, *args, **kwargs):
        # Preventing anyone from accessing a private blog through 
        # its id in the address bar
        if self.get_object().private:
            user = self.request.user
            if not user.is_authenticated or self.get_object().author != user:
                return HttpResponseRedirect(reverse_lazy('blog:blog-list'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = context['blog_entry'].get_category_list()
        context['breadcrumbs'] = enumerate(category_list)
        context['breadcrumbs_max'] = len(category_list)-1

        return context

class BlogEntryCreate(LoginRequiredMixin, CreateView):
    model = BlogEntry
    form_class = BlogEntryForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return super().post(request, *args, **kwargs)

    def get_login_url(self):
        login_url = reverse_lazy('user:login')

        return login_url

    def form_valid(self, form):
        blog = form.create()
        blog.author = self.request.user

        # If 'private' is specified in the url following the view's base url,
        # then this post is to be made private
        blog.private = self.kwargs.get('optional_param', '') == 'private'
        
        blog.save()
        return HttpResponseRedirect(reverse_lazy('blog:blog-detail', kwargs = {
            'pk': blog.id
        }))

    def form_invalid(self, form):
        print(form.cleaned_data['text_entry'])
        return HttpResponseRedirect(reverse_lazy('blog:blog-list'))
        
class BlogEntryUpdate(LoginRequiredMixin, UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm

    def form_valid(self, form):
        blog = form.update()
        blog.save()
        return HttpResponseRedirect(reverse_lazy('blog:blog-detail', kwargs = {
            'pk': blog.id
        }))

class BlogEntryDelete(LoginRequiredMixin, DeleteView):
    model = BlogEntry
    success_url = reverse_lazy('blog:blog-list')

class MyPosts(View):
    template_name='blog/user_posts.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        blog_entries = list(BlogEntry.objects.all().filter(author=user))

        if self.request.user != user:
            # Filtering out private entries if the user is viewing another user's
            # blog
            blog_entries = list(filter(lambda entry: not entry.private, blog_entries))

        blog_entries = sorted(blog_entries, key=attrgetter('date_of_submission'))

        blog_entries.reverse()

        context = {
            'blogs': blog_entries,
            'user_viewed': user
        }

        return render(request, self.template_name, context)