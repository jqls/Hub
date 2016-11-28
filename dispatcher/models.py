# coding=utf-8
from __future__ import unicode_literals

import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Mission(models.Model):
    name = models.CharField(max_length=30)
    guid = models.UUIDField(auto_created=True, default=uuid.uuid4)
