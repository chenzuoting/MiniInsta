from django.urls import path

from Insta.views import HelloWorld, PostListView

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
    path('home/', PostListView.as_view(), name='home'),
]