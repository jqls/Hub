# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-22 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0005_auto_20161218_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='processor',
            name='is_visualization',
            field=models.BooleanField(default=False),
        ),
    ]
