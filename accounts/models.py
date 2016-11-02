from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from sorl.thumbnail import ImageField
from helpers.file import random_name_with_file_field


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile')
    photo = ImageField(
        blank=True, null=True,
        upload_to=random_name_with_file_field
    )
    about = models.TextField(max_length=2000, blank=True, null=True)
