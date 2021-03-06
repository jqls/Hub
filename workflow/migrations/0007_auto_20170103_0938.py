# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_processor_is_visualization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_id', models.IntegerField()),
                ('db_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParameterDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='database_parameters', to='workflow.Database')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='parameter',
            name='belong_to',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='parameter',
            name='stage',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='processor',
            name='algorithm_category_id',
            field=models.IntegerField(default=0),
        ),
    ]
