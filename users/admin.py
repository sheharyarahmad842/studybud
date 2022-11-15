from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'bio', 'avatar')}),
    )
    model = CustomUser
    list_display = ['username', 'email', 'name']
    

admin.site.register(CustomUser, CustomUserAdmin)