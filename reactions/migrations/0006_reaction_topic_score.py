# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0005_auto_20161104_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='topic_score',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
