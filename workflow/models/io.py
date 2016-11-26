from django.db import models

from basic import DataType, BasicModel


class Channel(BasicModel):
    data_type = models.ForeignKey('DataType')

    class Meta:
        abstract = True


class InputChannel(Channel):
    processor = models.ForeignKey('Processor', related_name='inputs')

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        assert 'processor' in kwargs.keys()
        processor = kwargs['processor']
        data_type = DataType.objects.get(pk=attributes['dataType'])
        channel = cls(data_type=data_type, processor=processor)
        channel.save()
        return channel

    def to_dict(self):
        return {
            'id': self.pk,
            'processor_id': self.processor.id,
        }


class OutputChannel(Channel):
    processor = models.ForeignKey('Processor', related_name='outputs')

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        assert 'processor' in kwargs.keys()
        processor = kwargs['processor']
        data_type = DataType.objects.get(pk=attributes['dataType'])
        channel = cls(data_type=data_type, processor=processor)
        channel.save()
        return channel

    def to_dict(self):
        return {
            "id": self.pk,
            'processor_id': self.processor.id,
        }
