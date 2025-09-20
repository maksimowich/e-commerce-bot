from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from loguru import logger

from project.settings import SUPERUSER_NAME, SUPERUSER_PASSWORD


class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username=SUPERUSER_NAME).exists():
            User.objects.create_superuser(
                username=SUPERUSER_NAME,
                password=SUPERUSER_PASSWORD,
            )
            logger.info("Superuser created successfully.")
        else:
            logger.info("Superuser already exists.")
