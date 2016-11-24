from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from parameter import Parameter
from processor import Processor
from basic import DataType


class Stream(models.Model):
    data_type = models.ForeignKey(DataType)
    processor = models.ForeignKey(Processor)

    class Meta:
        abstract = True


class Input(Stream):
    parameters = GenericRelation(Parameter)


class Output(Stream):
    parameters = GenericRelation(Parameter)


class ConfiguredInput(models.Model):
    meta_input = models.ForeignKey('Input')


class ConfiguredOutput(models.Model):
    meta_output = models.ForeignKey('Output')
