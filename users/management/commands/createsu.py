from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                username=settings.SUPERUSER_USERNAME,
                name=settings.SUPERUSER_NAME,
                password=settings.SUPERUSER_PASSWORD,
            )
        print("Superuser has been created.")
