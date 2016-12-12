# coding=utf-8
import json

from channels.channel import Channel
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from models import Mission, Workflow, ProcesserOutputs, ConfiguredProcesserIO, ProcesserInputs, ConfiguredParameter, ConfiguredProcessor, Processor
from datetime import datetime
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

@csrf_exempt
def submit_mission_view(request):
    dict = {}
    info = ''
    try:
        if request.method == 'POST':
            startdate = datetime.now()
            mission = Mission(status=0, startDate=startdate,
                            endDate=datetime.now(),workflow=Workflow.objects.get(id=str(request.POST["workflow_id"])))
            mission.save()
            missionId = str(Mission.objects.get(startDate=startdate).id)
            Channel('submit_mission').send({'workflow_id':request.POST["workflow_id"], 'mission_id': missionId})
            dict['workflow_id'] = request.POST['workflow_id']
            dict['mission_id'] = missionId

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        dict['message'] = info
    return HttpResponse(json.dumps(dict))

@csrf_exempt
def get_parameters_view(request, parameter):
    info = {'parameters':[], 'number':0}
    # info = []
    try:
        if request.method == 'GET':
            paras = parameter.split('-')
            workflow_id, mission_id, processor_id = paras[0], paras[1], paras[2]
            parameters = ConfiguredParameter.objects.filter(configured_processor=ConfiguredProcessor.objects.get(workflow=Workflow.objects.get(id=int(workflow_id)),
                                                                                                              meta_processor=Processor.objects.get(id=int(processor_id))))

            for para in parameters:
                obj = {}
                obj['name'] = para.label
                obj['value'] = para.val
                info['parameters'].append(obj)
                info['number'] += 1
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    print info
    return HttpResponse(json.dumps(info), content_type='application/json')

@csrf_exempt
def get_inputs_view(request, parameter):
    info = {"inputs":[], "number":0}
    try:
        print parameter
        if request.method == 'GET':
            paras = parameter.split('-')
            workflow_id, mission_id, processor_id = paras[0], paras[1], paras[2]
            mission = Workflow.objects.get(id=int(workflow_id)).mission_set.get(id=int(mission_id))
            try:
                processor_io = mission.configuredprocesserio_set.get(processerID=int(processor_id))
                inputs = processor_io.processerinputs_set.all()
                for input in inputs:
                    obj = {}
                    obj['name'] = input.name
                    obj['path'] = input.path
                    info['inputs'].append(obj)
                    info['number'] += 1
            except:
                return HttpResponse(json.dumps(info))

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    print info
    return HttpResponse(json.dumps(info), content_type='application/json')

@csrf_exempt
def emit_outputs_view(request, parameter):
    dict = {}
    info = []
    try:
        if request.method == 'POST':
            print request.body
            body = json.loads(request.body)
            req = byteify(body)
            paras = parameter.split('-')
            workflow_id, mission_id, processor_id = paras[0], paras[1], paras[2]
            mission = Workflow.objects.get(id=int(workflow_id)).mission_set.get(id=int(mission_id))

            workflow = Workflow.objects.get(id=int(workflow_id)).to_dict()
            processoro = mission.configuredprocesserio_set.get_or_create(processorID=int(processor_id))
            processoro.mission = mission
            processoro.save()
            for output in req:
                ProcesserOutputs(name=output['name'], path=output['path'], processor=processoro).save()
                for connection in workflow['connections']:
                    if connection['output']['name'] == output['name']:
                        processori = mission.configuredprocesserio_set.get_or_create(processorID=int(connection['input']['processor_id']))
                        processori.mission = mission
                        processori.save()
                        ProcesserInputs(name=connection['input']['name'], path=output['path'], processor=processori).save()
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        dict['message'] = info


    return HttpResponse(json.dumps(info))
