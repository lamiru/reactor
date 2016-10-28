# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactions', '0007_auto_20161014_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='contents',
            field=models.TextField(db_index=True, verbose_name='contents'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='score',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='title'),
        ),
    ]