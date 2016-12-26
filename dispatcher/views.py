# coding=utf-8
import json

from channels.channel import Channel
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from models import Mission, Workflow, ProcessorOutputs, ConfiguredProcessorIO, ProcessorInputs, ConfiguredParameter, ConfiguredProcessor, Processor, InputChannel, OutputChannel, ConfiguredProcessorStatus
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import subprocess

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# def run_workflow(workflow_id):
#     dict = {}
#     info = ''
#     try:
#         startdate = datetime.now()
#         mission = Mission(status=0, startDate=startdate,
#                           endDate=datetime.now(),
#                           workflow=Workflow.objects.get(id=str(workflow_id)))
#         mission.save()
#         missionId = str(Mission.objects.get(startDate=startdate).id)
#         Channel('submit_mission').send({'workflow_id': workflow_id, 'mission_id': missionId})
#         dict['workflow_id'] = workflow_id
#         dict['mission_id'] = missionId
#
#     except:
#         import sys
#         info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         dict['message'] = info
#     return HttpResponse(json.dumps(dict))

@csrf_exempt
def submit_mission_view(request, parameter):
    dict = {}
    info = ''
    try:
        if request.method == 'POST':
            # print request.POST['workflow_id']
            startdate = datetime.now()
            mission = Mission(status=0, startDate=startdate,
                            endDate=datetime.now(),workflow=Workflow.objects.get(id=str(parameter)))
            mission.save()
            missionId = str(Mission.objects.get(startDate=startdate).id)
            Channel('submit_mission').send({'workflow_id':parameter, 'mission_id': missionId})
            dict['workflow_id'] = parameter
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
            workflow_id, mission_id, processor_id, flow_id = paras[0], paras[1], paras[2], paras[3]
            parameters = ConfiguredParameter.objects.filter(configured_processor=ConfiguredProcessor.objects.get(workflow=Workflow.objects.get(id=int(workflow_id)),
                                                                                                              meta_processor=Processor.objects.get(id=int(processor_id)),
                                                                                                                 flow_id=int(flow_id)))

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
            workflow_id, mission_id, processor_id, flow_id = paras[0], paras[1], paras[2], paras[3]
            workflow = Workflow.objects.get(id=int(workflow_id))
            mission = workflow.mission_set.get(id=int(mission_id))


            processor_io = ConfiguredProcessorIO.objects.get_or_create(processorID=int(processor_id), mission=mission,
                                                              configured_processor=ConfiguredProcessor.objects.get(flow_id=str(flow_id), workflow=workflow))
            try:
                if processor_io[1] == 1:
                    processor_io[0].save()
                inputs = processor_io[0].processorinputs_set.all()
                for input in inputs:
                    obj = {}
                    obj['name'] = input.name
                    obj['path'] = input.path
                    info['inputs'].append(obj)
                    info['number'] += 1
            except Exception, e:
                processor_io[0].delete()
                print e.message
                return HttpResponseBadRequest(e.message)

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
            body = json.loads(request.body)
            req = byteify(body)
            paras = parameter.split('-')
            workflow_id, mission_id, processor_id, flow_id = paras[0], paras[1], paras[2], paras[3]
            work_flow =  Workflow.objects.get(id=int(workflow_id))
            mission = work_flow.mission_set.get(id=int(mission_id))

            workflow = work_flow.to_dict()
            processoro = ConfiguredProcessorIO.objects.get_or_create(processorID=int(processor_id), mission=mission,
                                                                         configured_processor=ConfiguredProcessor.objects.get(flow_id=str(flow_id), workflow=work_flow))[0]
            processoro.save()
            print req
            for name in req.keys():
                ProcessorOutputs(name=name, path=req[name], processor=processoro).save()
                for connection in workflow['connections']:
                    if OutputChannel.objects.get(id=int(connection['output']['id'])).name == name and connection['output_processor_flow_id'] == flow_id:
                        print connection['input']['processor_id'], connection['input_processor_flow_id']
                        processori = ConfiguredProcessorIO.objects.get_or_create(processorID=int(connection['input']['processor_id']),mission=mission,
                                                                                     configured_processor=ConfiguredProcessor.objects.get(flow_id=connection['input_processor_flow_id'], workflow=work_flow))[0]
                        processori.save()
                        ProcessorInputs(name=InputChannel.objects.get(id=int(connection['input']['id'])).name, path=req[name], processor=processori).save()
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        dict['message'] = info

    return HttpResponse(json.dumps(info))

@csrf_exempt
def visualization_view(request, parameter):
    dict = {}
    info = "OK"
    try:
        if request.method == "GET":
            paras = parameter.split("-")
            paras2 = paras[:len(paras)-2]
            workflow_id, mission_id, processor_id, flow_id, port_id, line_num = paras[0], paras[1], paras[2], paras[3], paras[4], paras[5]

            resultdata = []
            dir = workflow_id + "-" + mission_id
            file = "-".join(paras2) + "-" + OutputChannel.objects.get(id=int(port_id)).name + ".text"
            path = "/user/spark/result_data/" + dir + "/" + file
            cmd_header = "sudo -u spark hdfs dfs -cat " + path
            proc = subprocess.Popen(cmd_header, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            num = 0
            while True:
                line = proc.stdout.readline()
                if line == '':
                    break
                line = line.replace(")", "").replace("(", "").replace("\n", "")
                if line == '':
                    break
                resultdata.append(line)
                num += 1
                if num == int(line_num):
                    break
            print num
            return HttpResponse(json.dumps(resultdata))
    except:
        import  sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

    dict['message'] = info

    return HttpResponse(json.dumps(dict))

@csrf_exempt
def processor_status_view(request, parameter):
    dict = {}
    info = "OK"
    try:
        if request.method == "GET":
            paras = parameter.split("-")
            # paras2 = paras[:len(paras)-2]
            print parameter
            workflow_id, mission_id = paras[0], paras[1]

            resultdata = [status.to_dict() for status in ConfiguredProcessorStatus.objects.filter(targetWorkflow_id=int(workflow_id),targetMission_id=int(mission_id))]
            # print resultdata
            return HttpResponse(json.dumps(resultdata))
    except:
        import  sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

    dict['message'] = info

    return HttpResponse(json.dumps(dict))
