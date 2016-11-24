# coding=utf-8

from django.db import models


# 用来表示系统中有的基础数据类型
class DataType(models.Model):
    type_name = models.CharField(max_length=10)
    slug = models.SlugField()
