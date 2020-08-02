from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

# forms defined here handles user inputs

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Build the form base on model InstaUser
        # UserCreationForm is based on mode User
        # CustomUserCreationForm is based on mode InstaUser
        model = InstaUser
        fields = ('username', 'email', 'profile_pic')