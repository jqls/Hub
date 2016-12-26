# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from workflow.models.processor import Processor, Category, ProcessorCategory
from workflow.models.workflow import Workflow
from dispatcher.models import Mission
from django.views.decorators.csrf import csrf_exempt

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def generic_get(request, model_cls):
    # todo: need pagination option
    assert request.method == 'GET'
    pk = request.GET.get('id', None)
    workflow_id = request.GET.get('workflow_id', None)
    if pk is not None:
        result = get_object_or_404(model_cls, pk=pk)
        result = result.to_dict()
    elif workflow_id is not None:
        if int(request.GET['workflow_id']) == 0:
            result = [model_cls.to_sample_dict() for model_cls in model_cls.objects.all()]
        elif int(request.GET['workflow_id']) != 0:
            result = model_cls.objects.get(id=int(int(request.GET['workflow_id']))).to_dict()
    else:
        result = [model_cls.to_dict() for model_cls in model_cls.objects.all()]
    print result
    return HttpResponse(content=json.dumps(result), content_type='application/json')

# def workflow_get(request, model_cls):
#     # todo: need pagination option
#     assert request.method == 'GET'
#     pk = request.GET.get('id', None)
#     if pk is not None:
#         result = get_object_or_404(model_cls, pk=pk)
#         result = result.to_dict()
#     elif int(request.GET['workflow_id']) == 0:
#         result = [model_cls.to_sample_dict() for model_cls in model_cls.objects.all()]
#     elif int(request.GET['workflow_id']) != 0:
#         result = model_cls.objects.get(id=int(int(request.GET['workflow_id']))).to_dict()
#
#     return HttpResponse(content=json.dumps(result), content_type='application/json')

@csrf_exempt
def workflow_rest(request):
    if request.method == 'POST':
        try:
            attributes = json.loads(request.body)
            attributes = byteify(attributes)
            print attributes
            workflow_id = Workflow.create_from_json_dict(attributes)
        except Exception, e:
            print e.message
            return HttpResponseBadRequest(e)
        return HttpResponse(json.dumps({"workflow_id": workflow_id}))
    elif request.method == 'GET':
        return generic_get(request, Workflow)
    return HttpResponseNotFound(content='not found')

@csrf_exempt
def mission_rest(request, mission_id):
    if request.method == 'GET':
        result = [mission.to_dict() for mission in Workflow.objects.get(id=int(request.GET['workflow_id'])).mission_set.all()]
        return HttpResponse(content=json.dumps(result), content_type='application/json')
    elif request.method == 'POST':
        try:
            Mission.objects.get(id=int(mission_id)).delete()
        except Exception, e:
            print e.message
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return HttpResponseNotFound(content='not found')

@csrf_exempt
def processor_rest(request, info):
    if request.method == "GET":
        return generic_get(request, Processor)
    elif request.method == "POST":
        try:
            attributes = json.loads(info)
            # print attributes
            attributes['is_visualization'] = False if attributes['is_visualization'] == '0' else True
            # print attributes
            attributes['execFile'] = request.FILES.get('file', None)
            print request.FILES.get('file', None).name
            # print info
            Processor.create_from_json_dict(attributes)
        except Exception, e:
            print e.message
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return HttpResponseNotFound()

@csrf_exempt
def processor_category_rest(request):
    rollback = []
    if request.method == "GET":

        info = Category.objects.get(category_id=-1).to_dict()
        return HttpResponse(content=json.dumps(info), content_type='application/json')

    elif request.method == "POST":
        try:
            print request.body
            attributes_json = json.loads(request.body.decode("utf-8"))
            Category.delete_old(children=Category.objects.get(category_id=-1).children.all())
            for attr in attributes_json:
                a = Category.create_from_json_dict(attr, parent=Category.objects.get(category_id=-1))
                rollback.append(a)
        except Exception, e:
            for item in rollback:
                item.delete()
            print e.message
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return  HttpResponseNotFound()

@csrf_exempt
def processor_category_delete(request):
    if request.method == "POST":
        try:
            print request.body
            attributes_json = json.loads(request.body.decode("utf-8"))
            # ProcessorCategory.delete_old(children=ProcessorCategory.objects.get(name=attributes_json["name"]).children.all())
            Category.objects.get(category_name=attributes_json["name"]).delete()
            ProcessorCategory.objects.get(name=attributes_json["name"]).delete()
        except Exception, e:
            print e.message
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return  HttpResponseNotFound()