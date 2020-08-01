from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from Insta.models import InstaUser, Post

# Create your views here.

class HelloWorld(TemplateView):
    template_name = 'helloworld.html'

class PostListView(ListView):
    model = Post
    template_name = 'home.html'