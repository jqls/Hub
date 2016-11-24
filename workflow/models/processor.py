import json

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from workflow import Workflow
from parameter import Parameter


class Processor(models.Model):
    name = models.CharField()
    parameters = GenericRelation(Parameter)

    def configure(self, workflow):
        pass

    def to_dict(self):
        return {}

    def to_json(self):
        return json.dumps(self.to_dict())


class ConfiguredProcessor(models.Model):
    uuid = models.UUIDField(auto_created=True)
    meta_processor = models.ForeignKey(Processor)
    workflow = models.ForeignKey(Workflow)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {}
