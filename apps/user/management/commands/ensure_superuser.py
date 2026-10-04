import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the configured Django superuser if it does not exist."

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        phone = os.environ.get("DJANGO_SUPERUSER_PHONE") or None

        if not email or not password:
            raise CommandError(
                "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set."
            )

        user_model = get_user_model()
        existing_user = user_model.objects.filter(email=email).first()
        if existing_user:
            if not existing_user.is_superuser:
                raise CommandError(
                    f"A non-superuser account already exists for {email}."
                )
            self.stdout.write(f"Superuser {email} already exists.")
            return

        user_model.objects.create_superuser(
            email=email,
            password=password,
            phone=phone,
        )
        self.stdout.write(self.style.SUCCESS(f"Created superuser {email}."))