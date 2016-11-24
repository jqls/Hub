from django.db import models

from io import ConfiguredInput, ConfiguredOutput


class Connection(models.Model):
    input = models.ForeignKey(ConfiguredInput)
    output = models.ForeignKey(ConfiguredOutput)
    workflow = models.ForeignKey('Workflow', related_name='connections')


class Workflow(models.Model):
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(auto_created=True)
    submit_time = models.DateTimeField(auto_now_add=True)
