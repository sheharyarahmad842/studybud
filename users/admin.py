from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# For language translations
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """Shows the admin page for users"""

    list_display = ["email", "username", "name", "is_active", "is_staff", "last_login"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Details"),
            {
                "fields": (
                    "username",
                    "name",
                )
            },
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    readonly_fields = ("last_login",)
    ordering = ["id"]


class ProfileAdmin(admin.ModelAdmin):
    """Shows the admin page for profiles"""

    list_display = ["name", "username", "email", "avatar", "created_on", "modified_on"]
    raw_id_fields = ["user"]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
