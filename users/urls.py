from django.urls import path
from .views import user_profile, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("<uuid:pk>/", user_profile, name="profile"),
    path(
        "update_profile/<uuid:pk>/", ProfileUpdateView.as_view(), name="update_profile"
    ),
]
