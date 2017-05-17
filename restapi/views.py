from django.shortcuts import render

# Create your views here.
from dispatcher.models import Mission
from rest_framework import viewsets
from django.db.models import Q
from serializers import MissionSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
import json

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

@csrf_exempt
def Mission_list(requset):

    # if requset.method == 'GET':
    #     missions = Mission.objects.all()
    #     serializer = MissionSerializer(missions, many=True)
    #     return JsonResponse(serializer.data, safe=False)
    #
    # if requset.method == 'POST':
    #     data = JSONParser.parse(requset)
    #     serializer = MissionSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, 400)
    extend_conditions = {}
    extend_conditions['workflow_id'] = 29
    response = generic_list(requset, Mission, MissionSerializer, extend_conditions)
    return response

@csrf_exempt
def Mission_detail(requset, id):
    # try:
    #     mission = Mission.objects.get(id=id)
    # except Mission.DoesNotExist:
    #     return HttpResponse(status=404)
    #
    # if requset.method == 'GET':
    #     serializer = MissionSerializer(mission)
    #     return JsonResponse(serializer.data)
    #
    # if requset.method == 'PUT':
    #     data = JSONParser().parse(requset)
    #     serializer = MissionSerializer(mission, data = data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)
    response = generic_detail(requset, id, None, Mission, MissionSerializer)
    return response

@csrf_exempt
def Mission_detail_v2(request, id1, id2):
    response = generic_detail(request, id1, id2, Mission, MissionSerializer)
    return response

def generic_list(request, model_cls, serializer_cls, extend_conditions = {}):

    # serializer_context = {
    #     'request': Request(request)
    # }
    try:
        if request.method == 'GET':
            columns = request.GET.get('columns', None)
            parameters = dict(request.GET)
            if parameters.has_key("columns"):
                del parameters['columns']
                for key in parameters.keys():
                    parameters[key] = parameters[key][0]
            # print str(columns).split(",")
            parameters.update(extend_conditions)
            print parameters
            results = model_cls.objects.all() if parameters == {} else model_cls.objects.filter(**parameters)
            serializer = serializer_cls(results, many=True)
            if columns:
                # print [i.name for i in model_cls._meta.fields if i.name not in str(columns).split(",")]
                for result in serializer.data:
                    for key in [i.name for i in model_cls._meta.fields if i.name not in str(columns).split(",")]:
                        if result.has_key(key):
                            result.pop(key)
            return JsonResponse(serializer.data, safe=False)

        if request.method == 'POST':
            print request.body
            data = json.loads(request.body)
            print data
            serializer = serializer_cls(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, 400)
        return JsonResponse("Not found operation", 501)
    except Exception, e:
        return JsonResponse(e.message, 501)

def generic_detail(request, id1, id2, model_cls, serializer_cls):
    try:
        if id2 == None:
            obj = model_cls.objects.filter(id=id1)
        else:
            obj = model_cls.objects.get(id=id1, status=id2)
    except model_cls.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        columns = request.GET.get('columns', None)
        print columns
        serializer = serializer_cls(obj, many=True)
        if columns:
            # print [i.name for i in model_cls._meta.fields if i.name not in str(columns).split(",")]
            for result in serializer.data:
                for key in [i.name for i in model_cls._meta.fields if i.name not in str(columns).split(",")]:
                    if result.has_key(key):
                        result.pop(key)
                print result

        return JsonResponse(serializer.data, safe=False)

    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = serializer_cls(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("Not found operation", status=501)


# def generic_list(request, model_cls):
#     # todo: need pagination option
#     assert request.method == 'GET'
#     pk = request.GET.get('id', None)
#     workflow_id = request.GET.get('workflow_id', None)
#     if pk is not None:
#         result = get_object_or_404(model_cls, pk=pk)
#         result = result.to_dict()
#     elif workflow_id is not None:
#         if int(request.GET['workflow_id']) == 0:
#             result = [model_cls.to_sample_dict() for model_cls in model_cls.objects.all()]
#         elif int(request.GET['workflow_id']) != 0:
#             result = model_cls.objects.get(id=int(int(request.GET['workflow_id']))).to_dict()
#     else:
#         result = [model_cls.to_dict() for model_cls in model_cls.objects.all()]
#     print result
#     return HttpResponse(content=json.dumps(result), content_type='application/json')