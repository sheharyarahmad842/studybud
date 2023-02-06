from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from users.models import Profile

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, related_name="rooms", null=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    participants = models.ManyToManyField(
        Profile, related_name="participants", blank=True
    )
    description = models.TextField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Room, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("base:room_detail", kwargs={"slug": self.slug})


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    body = models.CharField("Add a Comment", max_length=500)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_on", "-created_on"]

    def __str__(self):
        return self.body[:50]
