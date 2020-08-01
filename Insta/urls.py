from django.urls import path

from Insta.views import HelloWorld, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
    path('home/', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]