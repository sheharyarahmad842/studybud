from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from .models import Profile

User = get_user_model()


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)


# Signal to delete user if profile is deleted
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def save_social_user_name(sender, instance, created, **kwargs):
    if created:
        # Grabbing data from social account to create profile for that user
        user = User.objects.get(id=instance.user.id)
        user.name = instance.extra_data.get("name")
        user.save()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
post_save.connect(save_social_user_name, sender=SocialAccount)
