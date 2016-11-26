# coding=utf-8
from django.db import models
from basic import BasicModel
from processor import Processor
from io import InputChannel, OutputChannel


class Connection(BasicModel):
    input = models.ForeignKey('InputChannel')
    output = models.ForeignKey('OutputChannel')
    workflow = models.ForeignKey('Workflow', related_name='connections')
    import uuid as uid
    uuid = models.UUIDField(auto_created=True, default=uid.uuid4)

    def to_dict(self):
        return {
            'id': self.pk,
            'uuid': self.uuid.hex,
            'input': self.input.to_dict(),
            'output': self.output.to_dict(),
        }


class Workflow(BasicModel):
    name = models.CharField(max_length=200)
    submit_time = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        result = {
            'name': self.name,
            'submitTime': self.submit_time.isoformat(),
            'connections': [connection.to_dict() for connection in self.connections.all()],
            'parameters': [parameter.to_dict() for parameter in self.parameters.all()]
        }
        return result

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        workflow = cls.objects.create()

        configured_param = []
        connections = []
        try:
            workflow.name = attributes['name']
            workflow.save()
            # todo: 对代码进行优化，获得性能提升
            for processor_attributes in attributes['processors']:
                processor = Processor.objects.get(pk=processor_attributes['id'])
                param_dict = {}
                for param in processor.params.all():
                    param_dict[param.label] = param
                for param_label, param_value in processor_attributes['parameters'].items():
                    configured_param.append(param_dict[param_label].configure(workflow, param_value))

            for connection_dict in attributes['connections']:
                input_channel = InputChannel.objects.get(pk=int(connection_dict['from']['id']))
                output_channel = OutputChannel.objects.get(pk=int(connection_dict['to']['id']))
                connection = Connection(input=input_channel, output=output_channel, workflow=workflow)
                connections.append(connection)
                connection.save()

        except Exception, e:
            workflow.delete()
            for param in configured_param:
                param.delete()
            for connection in connections:
                connection.delete()
            raise e
        pass
