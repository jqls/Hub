# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 06:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0002_auto_20161123_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuredprocessor',
            name='meta_processor',
        ),
        migrations.RemoveField(
            model_name='configuredprocessor',
            name='mission_context',
        ),
        migrations.RemoveField(
            model_name='input',
            name='data_type',
        ),
        migrations.RemoveField(
            model_name='input',
            name='processor',
        ),
        migrations.RemoveField(
            model_name='output',
            name='data_type',
        ),
        migrations.RemoveField(
            model_name='output',
            name='processor',
        ),
        migrations.AlterUniqueTogether(
            name='parameter',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='processor',
        ),
        migrations.RemoveField(
            model_name='processor',
            name='category',
        ),
        migrations.DeleteModel(
            name='SelectionParameter',
        ),
        migrations.DeleteModel(
            name='TextParameter',
        ),
        migrations.DeleteModel(
            name='ConfiguredProcessor',
        ),
        migrations.DeleteModel(
            name='DataType',
        ),
        migrations.DeleteModel(
            name='Input',
        ),
        migrations.DeleteModel(
            name='MissionContext',
        ),
        migrations.DeleteModel(
            name='Output',
        ),
        migrations.DeleteModel(
            name='Parameter',
        ),
        migrations.DeleteModel(
            name='Processor',
        ),
        migrations.DeleteModel(
            name='ProcessorCategory',
        ),
    ]
