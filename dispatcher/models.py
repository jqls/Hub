# coding=utf-8
from __future__ import unicode_literals

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from workflow.models import *


class Mission(models.Model):
    startDate = models.DateTimeField(default=None)
    endDate = models.DateTimeField(default=None)
    status = models.IntegerField(default=0)
    workflow = models.ForeignKey(Workflow, null=True)

class Counter(models.Model):
    guid = models.CharField(max_length=200)
    counter = models.IntegerField(default=0)

class ConfiguredProcesserStatus(models.Model):
    status = models.IntegerField(default=0)
    targetProcessor = models.OneToOneField(ConfiguredProcessor, related_name='Status')
    targetWorkflow = models.ForeignKey(Workflow, null=True)

class ConfiguredProcesserIO(models.Model):
    processerID = models.IntegerField()
    mission = models.ForeignKey(Mission, null=True)

class ProcesserInputs(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    processor = models.ForeignKey(ConfiguredProcesserIO, null=True)

class ProcesserOutputs(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    processor = models.ForeignKey(ConfiguredProcesserIO, null=True)