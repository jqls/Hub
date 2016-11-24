# coding=utf-8
import json

from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from dispatcher.models import Processor


def post_mission(request):
    return HttpResponse("OK")


def get_mission(request, id):
    return HttpResponse("OK")


def get_processor(request, pk):
    processor_model = get_object_or_404(Processor, pk=pk)
    processor_dict = model_to_dict(processor_model)
    flat_map_fk = lambda x: [model_to_dict(instance) for instance in x]
    processor_dict['inputs'] = flat_map_fk(processor_model.inputs.all())
    processor_dict['outputs'] = flat_map_fk(processor_model.outputs.all())
    processor_dict['parameters'] = flat_map_fk(processor_model.parameters.all())
    data = json.dumps(processor_dict)
    return HttpResponse(content=data, content_type='application/json')
