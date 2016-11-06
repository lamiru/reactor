from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from sorl.thumbnail import ImageField
from helpers.file import random_name_with_file_field
from reactions.models import Reaction, Rating


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile')
    photo = ImageField(
        blank=True, null=True,
        upload_to=random_name_with_file_field
    )
    about = models.TextField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def photo_letters(self):
        return self.user.username[:2]

    def photo_bg_color(self):
        color_list = [
            'CCCCCC',
            'FFAA00',
            '00FFAA',
            'AA00FF',
            'AAFF00',
            '00AAFF',
            'FF00AA',
            '9900BB',
            'BB9900',
            '00BB99',
            '333333',
            '0033CC',
            'CC0033',
            '33CC00',
            '3300CC',
            'CC3300',
            '00CC33',
            '660099',
            '996600',
            '009966',
        ]
        return color_list[self.id % 20]

    def photo_default(self):
        return 'http://ipsumimage.appspot.com/140x45,{0}?l=l%20%20%20{1}%20%20%20l&f=ffffff'.format(
            self.photo_bg_color(),
            self.photo_letters(),
        )


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    active_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='active_notifications', blank=True, default='')
    passive_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='passive_notifications', blank=True, default='')
    CATEGORY_CHOICES = (
        ('RE', 'Reaction'),
        ('RA', 'Rating'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    reaction = models.ForeignKey(Reaction, null=True)
    rating = models.ForeignKey(Rating, null=True)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def url(self):
        if self.category == 'RA' or self.category == 'RE':
            return reverse('reactions:detail', args=[self.reaction.pk])
        return None

    def message(self):
        if self.category == 'RE':
            return '{0} reacted to <b>{1}</b>.'.format(self.active_user, self.reaction.title)
        elif self.category == 'RA':
            return '{0} rated <b>{1}</b>.'.format(self.active_user, self.reaction.title)
        return None
