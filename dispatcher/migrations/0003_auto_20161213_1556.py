# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0002_auto_20161213_1549'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConfiguredProcesserIO',
            new_name='ConfiguredProcessorIO',
        ),
        migrations.RenameModel(
            old_name='ConfiguredProcesserStatus',
            new_name='ConfiguredProcessorStatus',
        ),
        migrations.RenameModel(
            old_name='ProcesserInputs',
            new_name='ProcessorInputs',
        ),
        migrations.RenameModel(
            old_name='ProcesserOutputs',
            new_name='ProcessorOutputs',
        ),
        migrations.RenameField(
            model_name='configuredprocessorio',
            old_name='processerID',
            new_name='processorID',
        ),
    ]