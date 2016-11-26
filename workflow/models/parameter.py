# coding=utf-8
from __future__ import unicode_literals

import inspect

import sys
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from basic import BasicModel


# todo: 并不知道这个Magic会不会很影响性能，不顾目前能用就好
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
            'label': self.label,
            'hint': self.hint,
            'value': self.value,
            'optional': self.optional,
        }
        if self.parameter_input_object is not None:
            result.update(self.parameter_input_object.to_dict())
        return result

    class Meta:
        unique_together = ('content_type', 'object_id')


class ConfiguredParameter(BasicModel):
    meta_parameter = models.ForeignKey('Parameter')
    val = models.CharField(max_length=200)
    processor = models.ForeignKey('ConfiguredParameter', related_name='parameters')


class ProcessorCategory(BasicModel):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    description = models.TextField(verbose_name=u'简介')
    icon = models.CharField(max_length=20, verbose_name=u'图标名称')

    def __unicode__(self):
        return u'%s' % self.name
