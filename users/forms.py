from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    username = forms.CharField(max_length=50)
    avatar = forms.ImageField(
        label="Avatar",
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = Profile
        fields = ["name", "username", "avatar", "bio"]


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "name", "password1", "password2"]
