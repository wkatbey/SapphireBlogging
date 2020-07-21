from django.shortcuts import render
from django.views.generic import DeleteView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from blog.forms import EntryForm
from blog.models import BlogEntry, Category
from .helpers import get_blogs_by_category, remove_restricted_blogs
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from operator import attrgetter


class Portal(View):
    def get(self, request):

        posts = get_all_posts(BlogEntry.objects.all(), Reblog.objects.all())
        blogs = sorted(
            remove_restricted_blogs(blogs=blogs),
            key=attrgetter('date_of_submission'),
            reverse=True
        )


class CreateEntry(LoginRequiredMixin, View):
    template_url = 'blog/entry-form.html'

    def get_login_url(self):
        login_url = reverse_lazy('user:login')

        return login_url

    def get(self, request):
        context = {
            entryCreation: True
        }

        return TemplateResponse(request, template_url, context)


    def post(self, request):
        form = EntryForm(request.POST)

        if form.is_valid():
            entry = form.create()

            url = reverse_lazy('blog:entry-detail', kwargs={
                'pk': entry.id
            })

            return HttpResponseRedirect(url)

        context = {
            'error_messages': form.error_messages
        }

        return TemplateView(request, self.template_url, context)


class UpdateEntry(LoginRequiredMixin, View):
    template_url = 'blog/entry-form.html'

    def get_login_url(self):
        login_url = reverse_lazy('user:login')

        return login_url

    def get(self, request):
        context = {
            entryCreation: False
        }

        return TemplateResponse(request, template_url, context)

    def post(self, request):
        form = EntryForm(request.POST)

        if form.is_valid():
            entry = form.update()
            url = reverse_lazy('blog:entry-detail', kwargs={
                'pk': entry.id
            })

            return HttpResponseRedirect(url)
   
        
        context = {
            'error_messages': form.error_messages
        }

        return TemplateView(request, self.template_url, context)


class DeleteEntry(LoginRequiredMixin, DeleteView):
    model = BlogEntry
    success_url = reverse_lazy('blog:blog-list')


class EntryDetail(DetailView):
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
        context['breadcrumbs_max'] = len(category_list) - 1

        return context


class MyPosts(View):
    template_url = 'blog/user_posts.html'

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

        return render(request, self.template_url, context)


class PostsByCategory(View):
    template_url = 'blog/Entry_list_category.html'

    def get(self, request, pk):
        category_id = pk
        category = Category.objects.get(pk=category_id)

        blogs = sorted(
            remove_restricted_blogs(
                blogs=get_blogs_by_category(category),
                user=self.request.user
            ),
            key=attrgetter('date_of_submission'),
            reverse=True
        )

        breadcrumbs = category.get_category_list()
        breadcrumbs_max = len(breadcrumbs) - 1

        breadcrumbs = enumerate(breadcrumbs)

        context = {
            'blogs': blogs,
            'breadcrumbs': breadcrumbs,
            'breadcrumbs_max': breadcrumbs_max,
            'category': category
        }

        return render(request, self.template_url, context)