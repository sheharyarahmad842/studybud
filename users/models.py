import uuid
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.urls import reverse


class UserManager(BaseUserManager):
    """Custom User Manager for User Model"""

    def create_user(self, email, username, name, password=None):
        """Create, save and return a new user"""
        user = self.model(
            email=self.normalize_email(email), username=username, name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        """Create, save and return a new super user"""
        user = self.create_user(
            email=email, username=username, name=name, password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Defines custom user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = [
        "username",
        "name",
    ]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name


# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(null=True, blank=True)
    avatar = CloudinaryField(
        null=True,
        blank=True,
        default="https://res.cloudinary.com/dvhxqdx5f/image/upload/v1675587286/default_xy0uwu.jpg",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_on", "-created_on"]

    def __str__(self):
        return f"{self.user.name}'s profile"

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    @property
    def name(self):
        return self.user.name

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email
