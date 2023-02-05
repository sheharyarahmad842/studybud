from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = CloudinaryField(
        null=True,
        blank=True,
        default="https://res.cloudinary.com/dvhxqdx5f/image/upload/v1675587286/default_xy0uwu.jpg",
    )
