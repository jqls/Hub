# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-16 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0005_auto_20161226_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='endDate',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='startDate',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]