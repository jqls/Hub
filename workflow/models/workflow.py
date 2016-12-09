# coding=utf-8
from django.db import models
from basic import BasicModel
from processor import Processor
from io import InputChannel, OutputChannel
from .parameter import ConfiguredParameter
from .processor import ConfiguredProcessor


class Connection(BasicModel):
    input = models.ForeignKey('InputChannel')
    output = models.ForeignKey('OutputChannel')
    input_processor = models.ForeignKey('ConfiguredProcessor', related_name='input_connections')
    output_processor = models.ForeignKey('ConfiguredProcessor', related_name='output_connections')
    workflow = models.ForeignKey('Workflow', related_name='connections')

    def to_dict(self):
        return {
            'id': self.pk,
            'input': self.input.to_dict(),
            'input_processor_flow_id': self.input_processor.flow_id,
            'output_processor_flow_id': self.output_processor.flow_id,
            'output': self.output.to_dict(),
        }


class Workflow(BasicModel):
    name = models.CharField(max_length=200)
    submit_time = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        result = {
            'id': self.pk,
            'name': self.name,
            'submitTime': self.submit_time.isoformat(),
            'connections': [connection.to_dict() for connection in self.connections.all()],
            'parameters': [parameter.to_dict() for parameter in self.parameters.all()],
            'processors': [processor.to_dict() for processor in self.processors.all()]
        }
        return result

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        workflow = Workflow.objects.create()
        workflow.name = attributes['name']
        workflow.save()
        roll_back = []
        try:
            # todo: 对代码进行优化，获得性能提升
            for processor_attributes in attributes['processors']:
                processor = Processor.objects.get(pk=processor_attributes['id'])
                param_dict = {}
                # todo: bug here
                configured_processor = ConfiguredProcessor.objects.get_or_create(
                    meta_processor=processor,
                    workflow=workflow,
                    flow_id=processor_attributes['flow_id'],
                )[0]
                configured_processor.loc_x = processor_attributes['flow_id']
                configured_processor.save()
                roll_back.append(configured_processor)

                for param in processor.params.all():
                    param_dict[param.label] = param

                for param_label, param_value in processor_attributes['parameters'].items():
                    configured_parameter = param_dict[param_label].configure(
                        workflow,
                        param_value,
                        configured_processor)
                    roll_back.append(configured_parameter)

            for connection_dict in attributes['connections']:
                input_channel = InputChannel.objects.get(pk=int(connection_dict['to']['id']))
                output_channel = OutputChannel.objects.get(pk=int(connection_dict['from']['id']))
                input_processor = ConfiguredProcessor.objects.get(workflow=workflow,
                                                                  flow_id=connection_dict['to']['flow_id'])
                output_processor = ConfiguredProcessor.objects.get(workflow=workflow,
                                                                   flow_id=connection_dict['from']['flow_id'])
                connection = Connection(
                    input=input_channel,
                    output=output_channel,
                    workflow=workflow,
                    input_processor=input_processor,
                    output_processor=output_processor)
                roll_back.append(connection)
                connection.save()


        except Exception, e:
            for thing in roll_back:
                thing.delete()
            workflow.delete()
            raise e
