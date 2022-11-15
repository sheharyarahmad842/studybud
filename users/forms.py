from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'bio',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'username', 'email', 'bio']

class CustomSignupForm(UserCreationForm):
    # # name = forms.CharField(max_length=100, label='Full Name')
    # # bio = forms.TextInput()
    
    # def save(self, request):
    #     user =  super(CustomSignupForm, self).save(request)
    #     user.name = self.cleaned_data['name']
    #     # user.bio = self.cleaned_data['bio']
    #     return user

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'email', 'password1', 'password2']
