# coding=utf-8
from __future__ import unicode_literals

import json

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from processor import ConfiguredProcessor, Processor


class ParameterInput(models.Model):
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {}

    class Meta:
        abstract = True


class ParameterSelectionChoice(models.Model):
    choice = models.CharField(max_length=30)
    selection = models.ForeignKey('ParameterSelection', related_name='choices')

    def __unicode__(self):
        return u'%s' % self.choice

    def __repr__(self):
        return self.__unicode__()


class ParameterSelection(ParameterInput):
    def to_dict(self):
        result = {'choice': [choice for choice in self.choices.all()]}
        return result

    def to_json(self):
        return json.dumps(self.to_dict())


class ParameterText(ParameterInput):
    pass


class Parameter(models.Model):
    label = models.CharField(max_length=30)
    hint = models.CharField(max_length=130, blank=True, default="")
    value = models.CharField(max_length=225, blank=True, default="")
    optional = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parameter_object = GenericForeignKey()

    configurable_object = GenericForeignKey()

    def to_json(self):
        result = {
            'label': self.label,
            'hint': self.hint,
            'value': self.value,
            'optional': self.optional,
        }
        # MAGIC
        result.update(self.parameter_object.to_dict())
        return json.dumps(result)

    def __unicode__(self):
        return u'%s' % self.to_json()

    def __repr__(self):
        return self.__unicode__()

    class Meta:
        unique_together = ('content_type', 'object_id')


class ConfiguredParameter(models.Model):
    meta_parameter = models.ForeignKey('Parameter')
    val = models.CharField(max_length=200)
    processor = models.ForeignKey(ConfiguredProcessor, related_name='parameters')


# ProcessorCategory 用来表示Processor的类型，比如可以是：数据源、聚类算法、特征提取算法等
class ProcessorCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    description = models.TextField(verbose_name=u'简介')
    icon = models.CharField(max_length=20, verbose_name=u'图标名称')

    def __unicode__(self):
        return u'%s' % self.name
