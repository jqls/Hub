from django.db import models

from basic import DataType, BasicModel


class Channel(BasicModel):
    data_type = models.ForeignKey('DataType')

    class Meta:
        abstract = True


class InputChannel(Channel):
    processor = models.ForeignKey('Processor', related_name='inputs')
    name = models.CharField(max_length=30)

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        assert 'processor' in kwargs.keys()
        processor = kwargs['processor']
        data_type = DataType.objects.get(pk=int(attributes['dataType']))
        channel = cls(name=attributes['name'], data_type=data_type, processor=processor)
        channel.save()
        return channel

    def to_dict(self):
        return {
            'id': self.pk,
            'processor_id': self.processor.id,
        }


    class Meta:
        unique_together = ('processor', 'name')


class OutputChannel(Channel):
    processor = models.ForeignKey('Processor', related_name='outputs')
    name = models.CharField(max_length=30)

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        assert 'processor' in kwargs.keys()
        processor = kwargs['processor']
        data_type = DataType.objects.get(pk=int(attributes['dataType']))
        channel = cls(name=attributes['name'], data_type=data_type, processor=processor)
        channel.save()
        return channel

    def to_dict(self):
        return {
            "id": self.pk,
            'processor_id': self.processor.id,
        }

    class Meta:
        unique_together = (('processor', 'name'),)