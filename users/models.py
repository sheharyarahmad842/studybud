from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import uuid


class UserManager(BaseUserManager):
    """Custom User Manager for User Model"""

    def create_user(self, email, name, password=None):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """Create, save and return a new super user"""
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Defines custom user model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = [
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

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email
