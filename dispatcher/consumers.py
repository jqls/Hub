import time
import logging
import subprocess

from channels.channel import Channel
from models import *
import uuid
import monitor
import json

logger = logging.getLogger('django')


def submit_mission(message):
    workflowInfo = Workflow.objects.get(id=message['workflow_id']).to_dict()
    uuid2flowid = {}
    for i in workflowInfo['processors']:
        uid = uuid.uuid4()
        uuid2flowid[uid.hex] = i['flow_id']
        counter = Counter(guid=uid.hex)
        counter.save()
    while len(uuid2flowid.keys()):
        for UUID in uuid2flowid.keys():
            counter = Counter.objects.get(guid=UUID)
            inputs = -1
            processor_id = -1
            for proc in workflowInfo['processors']:
                if proc['flow_id'] == uuid2flowid[UUID]:
                    inputs = len(proc['inputs'])
                    processor_id = proc['id']
            if counter.counter == inputs:
                outputs = []
                for connection in workflowInfo['connections']:
                    if connection['output_processor_flow_id'] == uuid2flowid[UUID]:
                        for i in uuid2flowid.keys():
                            if uuid2flowid[i] == connection['input_processor_flow_id']:
                                outputs.append(i)
                                break
                Channel('processer_runner').send({'workflow_id':message['workflow_id'], 'mission_id':message['mission_id'],
                                                  'processor_id':processor_id, 'next_proc:':outputs})
                uuid2flowid.pop(UUID)
    # logger.info('send uuid %s' % uid.hex)
    # Channel('counter').send({'uuid': uid.hex})

def processor_runner(message):
    workflow_id = message['workflow_id']
    mission_id = message['mission_id']
    processor_id = message['processor_id']

    cmd_header = "sudo -u spark spark-submit "

    cmd_header = cmd_header + " --class " + "Main" + ' ' + Processor.objects.get(id=processor_id).exec_file.name
    # cmd_header = cmd_header + " " + jar
    cmd_header = cmd_header + " " + workflow_id + "-" + mission_id + "-" + processor_id

    app_ID = ''
    proc = subprocess.Popen(cmd_header, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = proc.stdout.readline()
        flag = line.find("Submitted application application_")
        if flag >= 0:
            start = line.find("application_")
            app_ID = line[start:]
        if not line:
            break
        print line
    proc.wait()

    mot = monitor.SparkMonitor('10.5.0.223', '8088')
    ret = mot.appInfo(app_ID)
    appinfo = mot.byteify(json.loads(ret[2]))
    if appinfo['app']['finalStatus'] == 'SUCCESSED':
        for UUID in message['next_proc']:
            counter = Counter.objects.get(guid=UUID)
            counter.counter = counter.counter + 1
            counter.save()

        processor = Workflow.objects.get(id=workflow_id).processors.all().get(id=processor_id)
        processor.Status.status = 3


