# coding=utf-8

from django.db import models


class BasicModel(models.Model):
    def to_dict(self):
        # todo: use magic here to provide generic method
        return {}

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        raise Exception('Not implement')

    class Meta:
        abstract = True


# 用来表示系统中有的基础数据类型
class DataType(BasicModel):
    type_name = models.CharField(max_length=10)
    slug = models.SlugField()
