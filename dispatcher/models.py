# coding=utf-8
from __future__ import unicode_literals

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from workflow.models import Workflow


class Mission(models.Model):
    startDate = models.DateTimeField(default=None)
    endDate = models.DateTimeField(default=None)
    status = models.IntegerField(default=0)
    workflow = models.ForeignKey(Workflow, null=True)

class Counter(models.Model):
    guid = models.CharField(max_length=200)
    counter = models.IntegerField(default=0)
