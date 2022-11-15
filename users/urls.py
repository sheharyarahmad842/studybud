from django.urls import path
from .views import user_profile, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', user_profile, name='profile'),
    path('update_profile/<int:pk>/', ProfileUpdateView.as_view(), name='update_profile'),
]
