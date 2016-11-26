# coding=utf-8
import json

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from basic import BasicModel
from parameter import Parameter
from io import InputChannel, OutputChannel


class Processor(BasicModel):
    name = models.CharField(max_length=140)
    exec_file = models.FileField(upload_to='exec_files', null=True)

    def to_dict(self):
        # todo：这里可以使用Magic
        result = {
            "id": self.pk,
            "name": self.name,
            "params": [param.to_dict() for param in self.params.all()],
            "inputs": [input_channel.to_dict() for input_channel in self.inputs.all()],
            "outputs": [output_channel.to_dict() for output_channel in self.outputs.all()]
        }
        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        processor = cls.objects.create()
        processor.save()
        processor.exec_file = attributes['execFile']
        try:
            for parameter_attributes in attributes['parameters']:
                Parameter.create_from_json_dict(parameter_attributes, processor=processor)
            for input_attributes in attributes['inputs']:
                InputChannel.create_from_json_dict(input_attributes, processor=processor)
            for output_attributes in attributes['outputs']:
                OutputChannel.create_from_json_dict(output_attributes, processor=processor)
        except Exception, e:
            processor.delete()
            raise e
        return processor


class ConfiguredProcessor(BasicModel):
    uuid = models.UUIDField(auto_created=True)
    meta_processor = models.ForeignKey('Processor')
    workflow = models.ForeignKey('Workflow')

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {}
