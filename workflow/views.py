# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from workflow.models.processor import Processor
from workflow.models.workflow import Workflow


def generic_get(request, model_cls):
    # todo: need pagination option
    assert request.method == 'GET'
    pk = request.GET.get('id', None)
    if pk is not None:
        result = get_object_or_404(model_cls, pk=pk)
        result = result.to_dict()
    else:
        result = [model_cls.to_dict() for model_cls in Processor.objects.all()]
    return HttpResponse(content=json.dumps(result), content_type='application/json')


def workflow_rest(request):
    if request.method == 'POST':
        try:
            attributes = json.loads(request.content)
            Workflow.create_from_json_dict(attributes)
        except Exception, e:
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    elif request.method == 'GET':
        return generic_get(request, Workflow)
    return HttpResponseNotFound()


def processor_rest(request):
    if request.method == "GET":
        return generic_get(request, Processor)
    elif request.method == "POST":
        try:
            attributes_json = request.POST['info']
            attributes = json.loads(attributes_json)
            attributes['execFile'] = request.FILES['execFile']

            Processor.create_from_json_dict(attributes)
        except Exception, e:
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return HttpResponseNotFound()
