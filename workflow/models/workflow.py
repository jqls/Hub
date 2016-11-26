from django.db import models

from basic import BasicModel


class Connection(BasicModel):
    input = models.ForeignKey('InputChannel')
    output = models.ForeignKey('OutputChannel')
    workflow = models.ForeignKey('Workflow', related_name='connections')


class Workflow(BasicModel):
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(auto_created=True)
    submit_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        workflow = cls.objects.create()
        workflow.save()
        try:
            pass
        except Exception, e:
            workflow.delete()
            raise e
        pass
