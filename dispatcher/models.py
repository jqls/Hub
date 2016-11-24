# coding=utf-8
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class MetaProcessorParameter(models.Model):
    name = models.CharField(max_length=30)
    hint = models.CharField(max_length=130, blank=True)

    class Meta:
        abstract = True


class SelectionParameter(MetaProcessorParameter):
    pass


class TextParameter(MetaProcessorParameter):
    pass


class Parameter(models.Model):
    processor = models.ForeignKey('Processor', related_name='parameters')

    class Meta:
        unique_together = (("content_type", "object_id",),)


class Processor(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    category = models.ForeignKey('ProcessorCategory', verbose_name='所属类别')
    jar_file = models.FilePathField(blank=True, default="")

    def validate_parameters(self, unknown_parameters):
        # type: (dict) -> bool
        for parameter in self.parameters.all():
            valid = parameter.optional
            if parameter.name in unknown_parameters:
                valid = parameter.validate(unknown_parameters[parameter.name])
            if not valid:
                return False
        return True


class DataType(models.Model):
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.display_name)


class Input(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    data_type = models.ForeignKey('DataType')
    optional = models.BooleanField(default=False)
    processor = models.ForeignKey('Processor', related_name='inputs')


class Output(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'名称')
    data_type = models.ForeignKey('DataType')
    processor = models.ForeignKey('Processor', related_name='outputs')


class ConfiguredProcessor(models.Model):
    meta_processor = models.ForeignKey('Processor')
    parameters = models.TextField()
    inputs = models.TextField()
    mission_context = models.ForeignKey('MissionContext')


class MissionContext(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'任务名称')
    uuid = models.UUIDField(auto_created=True)
    submit_time = models.DateTimeField(auto_now_add=True)
