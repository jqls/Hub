# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 07:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_category'),
        ('dispatcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuredprocesserio',
            name='configured_processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.ConfiguredProcessor'),
        ),
        migrations.AlterField(
            model_name='processerinputs',
            name='path',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='processeroutputs',
            name='path',
            field=models.CharField(max_length=200, null=True),
        ),
    ]