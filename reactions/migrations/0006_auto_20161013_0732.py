# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-13 07:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0005_auto_20161011_0922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='rator',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('user', 'reaction')]),
        ),
    ]