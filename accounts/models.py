from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from helpers.file import random_name_with_file_field


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(
        blank=True, null=True,
        upload_to=random_name_with_file_field
    )
    about = models.TextField(blank=True, null=True)
