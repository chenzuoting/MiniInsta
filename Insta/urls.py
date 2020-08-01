from django.urls import path

from Insta.views import HelloWorld

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
]