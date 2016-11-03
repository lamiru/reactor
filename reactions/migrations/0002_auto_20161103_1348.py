# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 13:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='user',
            new_name='rater',
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('rater', 'reaction')]),
        ),
    ]
