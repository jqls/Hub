# coding=utf-8
import json

from django.db import models
from basic import BasicModel
from parameter import Parameter
from io import InputChannel, OutputChannel


class Processor(BasicModel):
    name = models.CharField(max_length=140)
    exec_file = models.FileField(upload_to='exec_files', null=True)
    category = models.ForeignKey('ProcessorCategory', related_name='processors')

    def to_dict(self):
        # todo：这里可以使用Magic

        result = {
            "id": self.pk,
            "name": self.name,
            "params": [param.to_dict() for param in self.params.all()],
            "inputs": [input_channel.to_dict() for input_channel in self.inputs.all()],
            "outputs": [output_channel.to_dict() for output_channel in self.outputs.all()],
            "category": self.category.to_sequence()
        }
        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        processor = Processor(name=attributes['name'], exec_file=attributes['execFile'])
        category_path = attributes['category']
        categorys = category_path.split(">")
        parent = None
        for category in categorys:
            child = ProcessorCategory.objects.get_or_create(parent=parent, name=category)
            if child[1] == 1:
                child[0].save()
            parent = child[0]
        processor.category = parent
        # processor.exec_file = attributes['execFile']
        processor.save()
        rollback = []
        try:
            for parameter_attributes in attributes['parameters']:
                a = Parameter.create_from_json_dict(parameter_attributes, processor=processor)
                rollback.append(a)
            for input_attributes in attributes['inputs']:
                a = InputChannel.create_from_json_dict(input_attributes, processor=processor)
                rollback.append(a)
            for output_attributes in attributes['outputs']:
                a = OutputChannel.create_from_json_dict(output_attributes, processor=processor)
                rollback.append(a)
        except Exception, e:
            processor.delete()
            for item in rollback:
                item.delete()
            raise e
        return processor


class ConfiguredProcessor(BasicModel):
    meta_processor = models.ForeignKey('Processor')
    workflow = models.ForeignKey('Workflow', related_name='processors')
    flow_id = models.CharField(max_length=30, default=0)
    loc_x = models.FloatField(default=0.0)
    loc_y = models.FloatField(default=0.0)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.meta_processor.id,
            'flow_id': self.flow_id,
            'inputs': [input_channel.id for input_channel in self.meta_processor.inputs.all()],
            'outputs': [output_channel.id for output_channel in self.meta_processor.outputs.all()],
        }

class ProcessorCategory(BasicModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=20, verbose_name=u'图标名称')
    parent = models.ForeignKey('self', related_name='children', default=None, null=True)

    def to_sequence(self):
        path = self.name
        parent = self.parent
        while parent != None:
            path = parent.name + '>' + path
            parent = parent.parent

        return path
