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

    def to_dict(self):
        result = {
            "id": self.pk,
            "submit_time": str(self.startDate),
            "finish_time": str(self.endDate),
            "missionStatus": self.status,
            "workflow_name": self.workflow.name
        }
        return result

class Counter(models.Model):
    guid = models.CharField(max_length=200)
    counter = models.IntegerField(default=0)

class ConfiguredProcessorStatus(models.Model):
    status = models.IntegerField(default=0)
    targetProcessor = models.OneToOneField(ConfiguredProcessor, related_name='Status')
    targetWorkflow = models.ForeignKey(Workflow, null=True)
    targetMission = models.ForeignKey(Mission, null=True)

    def to_dict(self):
        result = {
            "processor_id": self.targetProcessor.meta_processor_id,
            "flow_id": self.targetProcessor.flow_id,
            "status": self.status,
        }
        return result

class ConfiguredProcessorIO(models.Model):
    processorID = models.IntegerField()
    mission = models.ForeignKey(Mission, null=True)
    configured_processor = models.ForeignKey(ConfiguredProcessor, null=True)

class ProcessorInputs(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, null=True)
    processor = models.ForeignKey(ConfiguredProcessorIO, null=True)

class ProcessorOutputs(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, null=True)
    processor = models.ForeignKey(ConfiguredProcessorIO, null=True)