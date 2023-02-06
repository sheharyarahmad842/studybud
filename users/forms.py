from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "name", "password1", "password2"]
