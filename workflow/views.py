# coding=utf-8
import json
import os, subprocess
from django.http.response import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from hub.settings import MEDIA_ROOT, HDFS_DATA_ROOT
from workflow.models.processor import Processor, Category, ProcessorCategory
from workflow.models.workflow import Workflow
from workflow.models.parameter import Parameter, ParameterDatabase
from workflow.models.basic import Database, Document
from dispatcher.models import Mission
from django.views.decorators.csrf import csrf_exempt
import pymysql

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def remove_item(path):
    if os.path.exists(path):
        os.remove(path)

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
            print attributes
            # attributes['is_visualization'] = False if attributes['is_visualization'] == '0' else True
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
def processor_category_rest(request, parameter):
    rollback = []
    if request.method == "GET":

        info = Category.objects.get(category_id=-1).to_dict()
        print info
        return HttpResponse(content=json.dumps(info), content_type='application/json')

    elif request.method == "POST":
        try:
            print parameter
            attributes_json = json.loads(parameter)
            attributes_json['image'] = request.FILES.get('image', None)
            # print request.FILES.get('image', None).name
            print attributes_json
            # Category.delete_old(children=Category.objects.get(category_id=-1).children.all())
            # for attr in attributes_json:
            a = Category.create_from_json_dict(attributes_json, parent=Category.objects.get(category_id=-1), image = attributes_json['image'])
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
            # attributes_json = json.loads(request.body.decode("utf-8"))
            # ProcessorCategory.delete_old(children=ProcessorCategory.objects.get(name=attributes_json["name"]).children.all())
            target = Category.objects.get(category_id=int(request.body))
            paths = []
            children = []

            def getProcessPaths(target, paths):
                category = target.ConfiguredCategory.all()
                for processors in category:
                    for processor in processors.processors.all():
                        paths.append(MEDIA_ROOT + str(processor.exec_file))

            getProcessPaths(target, paths)
            if target.picture_path.name:
                paths.append(MEDIA_ROOT + target.picture_path.name)

            for child in target.children.all():
                children.append(child)
                getProcessPaths(child, paths)
                if child.picture_path.name:
                    paths.append(MEDIA_ROOT + child.picture_path.name)

            while children != []:
                curr = children.pop()
                for child in curr.children.all():
                    children.append(child)
                    getProcessPaths(child, paths)
                    if child.picture_path.name:
                        paths.append(MEDIA_ROOT + child.picture_path.name)

            for path in paths:
                remove_item(path)
            print request.body
            target.delete()
            # ProcessorCategory.objects.get(category_id=attributes_json["name"]).delete()
        except Exception, e:
            print e.message
            return HttpResponseBadRequest(e.message)
        return HttpResponse()
    return  HttpResponseNotFound()

@csrf_exempt
def document_rest(request, info):
    if request.method == "POST":
        roll_back = []
        try:
            # print request.FILES
            attributes = json.loads(info)
            attributes['document'] = request.FILES.get('document', None)
            print request.FILES.get('document', None).name
            a = Document.create_from_json_dict(attributes)
            roll_back.append(a)
            cmd = "sudo -u spark hdfs dfs -copyFromLocal " + MEDIA_ROOT + a.document.name + " " + HDFS_DATA_ROOT
            print cmd
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
            remove_item(MEDIA_ROOT + a.document.name)
            a.file_path = HDFS_DATA_ROOT + attributes['document'].name
            a.save()
        except Exception, e:
            for a in roll_back:
                a.delete()
            print e.message
            return HttpResponse(json.dumps({"error": e.message}))
        return HttpResponse(json.dumps({"info": "OK"}))
    return HttpResponseNotFound

def mysql_rest(attributes, operation):
    data = {}
    try:
        # print type(operation)
        host = attributes['parameters']['host']
        port = attributes['parameters']['port']
        password = attributes['parameters']['password']
        user = attributes['parameters']['user']
        dbase = attributes['parameters']['dbase']
        conn = pymysql.connect(host=host, port=int(port), user=user, passwd=password, db=dbase)
        cur = conn.cursor()
        if operation == 0:
            cur.execute("show tables")
            data['table_list'] = []
            for r in cur:
                print r[0]
                data['table_list'].append(r[0])
            if data['table_list'] != []:
                data['url'] = '/workflow/sql/1/'

        elif operation == 1:
            print attributes['parameters']['tablelist']
            table_name = attributes['parameters']['tablelist']
            cur.execute("show columns from {}".format(table_name))
            data['col_list'] = []
            for r in cur:
                data['col_list'].append(r[0])
                print r[0]
        cur.close()
        conn.close()
    except pymysql.Error, e:
        print e.args[0], e.args[1]
        return json.dumps([e.message])
    return data

@csrf_exempt
def sql_rest(request, operation):
    data = None
    try:
        if request.method == "POST":
            try:
                attributes_json = json.loads(request.body.decode("utf-8"))
                print attributes_json
                if attributes_json["ac_id"] == 1:
                    if attributes_json["db_id"] == 1:
                        # print attributes_json
                        data = mysql_rest(attributes_json, int(operation))
                    else:
                        return HttpResponseBadRequest()
                else:
                    return HttpResponseBadRequest()
            except Exception, e:
                print e.message
                return HttpResponse(json.dumps(e.message))
        elif request.method == "GET":
            try:
                data = {}
                data["parameters"] = [parameter.to_dict() for parameter in Parameter.objects.filter(belong_to=request.GET["database"], processor_id=int(request.GET["processor_id"]),
                                                                                          stage=int(operation))]

            except Exception, e:
                print e.message
                return HttpResponse(json.dumps(e.message))
    except Exception, e:
        return HttpResponseBadRequest(json.dumps(e.message))
    return HttpResponse(json.dumps(data))