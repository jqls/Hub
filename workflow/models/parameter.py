# coding=utf-8
from __future__ import unicode_literals

import inspect
import sys
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from basic import BasicModel, Document


# todo: 并不知道这个Magic会不会很影响性能，目前能用就好
def valid_parameters():
    parameters_types = {}
    current_modules = sys.modules[__name__]
    for name, obj in inspect.getmembers(current_modules):
        if inspect.isclass(obj) and issubclass(obj, ParameterInput):
            parameters_types[obj.parameter_type] = obj
    return parameters_types


def is_valid_parameter(parameter_type):
    return parameter_type in valid_parameters().keys()


class ParameterInput(BasicModel):
    parameter_type = "meta"

    def to_dict(self, result=None):
        if result is None:
            result = {}
        result.update({"parameterType": self.parameter_type})
        return result

    class Meta:
        abstract = True


class ParameterSelectionChoice(BasicModel):
    choice = models.CharField(max_length=30)
    selection = models.ForeignKey('ParameterSelection', related_name='choices')

    def __unicode__(self):
        return u'%s' % self.choice

    def __repr__(self):
        return self.__unicode__()


class ParameterSelection(ParameterInput):
    parameter_type = "selection"

    def to_dict(self, result=None):
        result = {"choices": [str(choice) for choice in self.choices.all()]}
        return super(ParameterSelection, self).to_dict(result)

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        selection = ParameterSelection()
        selection.save()
        for choice in attributes['choices']:
            selection_choice = ParameterSelectionChoice(choice=choice, selection=selection)
            selection_choice.save()
        return selection


class ParameterText(ParameterInput):
    parameter_type = "text"

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        text = ParameterText()
        text.save()
        return text

class ParameterFileList(ParameterInput):
    parameter_type = "filelist"

    def to_dict(self, result=None):
        result = {"filelist": [file.to_dict() for file in Document.objects.all()]}
        return super(ParameterFileList, self).to_dict(result)

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        filelist = ParameterFileList()
        filelist.save()
        return filelist


# noinspection PyUnresolvedReferences
class Parameter(BasicModel):
    label = models.CharField(max_length=30)
    hint = models.CharField(max_length=130, blank=True, default="")
    value = models.CharField(max_length=225, blank=True, default="")
    optional = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parameter_input_object = GenericForeignKey()

    processor = models.ForeignKey('Processor', related_name='params')

    @classmethod
    def create_from_json_dict(cls, parameter_attributes, **kwargs):
        assert 'processor' in kwargs.keys()
        processor = kwargs['processor']
        assert processor is not None

        parameter_input_model = valid_parameters().get(parameter_attributes['parameterType'], None)
        if parameter_input_model is None:
            raise Exception('Parameter type %s is not expected.' % parameter_attributes['type'])
        parameter = None
        parameter_input = None
        try:
            parameter_input = parameter_input_model.create_from_json_dict(parameter_attributes)
            parameter = Parameter(
                label=parameter_attributes['label'],
                hint=parameter_attributes.get('hint', ''),
                value=parameter_attributes.get('value', ''),
                optional=parameter_attributes.get('optional', True),
                parameter_input_object=parameter_input,
                processor=processor
            )
            parameter.save()
        except Exception, e:
            if parameter_input is not None:
                parameter_input.delete()
            if parameter is not None:
                parameter.delete()
            raise e
        return parameter

    def to_dict(self):
        result = {
            'id': self.pk,
            'key': self.label,
            'label': self.label,
            'hint': self.hint,
            'description': self.hint,
            'value': self.value,
            'required': self.optional,
            'optional': self.optional,
            'controlType': self.parameter_input_object.parameter_type,
        }
        if self.parameter_input_object is not None:
            result.update(self.parameter_input_object.to_dict())
        return result

    def configure(self, workflow, value, configure_processor):
        # todo: 需要进行参数检查，设置值限制
        configured_parameter = ConfiguredParameter(
            meta_parameter=self,
            label=self.label,
            val=value,
            workflow=workflow,
            configured_processor=configure_processor,
        )
        configured_parameter.save()
        return configured_parameter

    class Meta:
        unique_together = (('content_type', 'object_id'), ('label', 'processor'))


class ConfiguredParameter(BasicModel):
    meta_parameter = models.ForeignKey('Parameter')
    label = models.CharField(max_length=30, default="")
    val = models.CharField(max_length=200)
    configured_processor = models.ForeignKey('ConfiguredProcessor', related_name='parameters')
    workflow = models.ForeignKey('Workflow', related_name='parameters')

    def to_dict(self):
        return {
            'processor_id': self.configured_processor.meta_processor.pk,
            'flow_id': self.configured_processor.flow_id,
            'label': self.label,
            'val': self.val,
        }


