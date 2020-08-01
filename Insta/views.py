from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from Insta.models import InstaUser, Post

# Create your views here.

class HelloWorld(TemplateView):
    template_name = 'helloworld.html'

class PostListView(ListView):
    model = Post
    template_name = 'home.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    #cannot use reverse here, we are trying to redirect during delete process, which is invalid
    #with reverse_lazy, we are redirecting and let delete running in the back
    success_url = reverse_lazy("home")