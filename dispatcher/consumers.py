import time
import logging
import subprocess

from channels.channel import Channel
from models import Workflow, Counter, Processor, ConfiguredProcesserStatus
import uuid
import monitor
import json

logger = logging.getLogger('django')


def submit_mission(message):
    workflowInfo = Workflow.objects.get(id=message['workflow_id']).to_dict()
    uuid2flowid = {}
    rollback = []
    for i in workflowInfo['processors']:
        uid = uuid.uuid4()
        uuid2flowid[uid.hex] = i['flow_id']
        counter = Counter(guid=uid.hex)
        counter.save()
        rollback.append(counter)
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
                Channel('processor_runner').send({'workflow_id':message['workflow_id'], 'mission_id':message['mission_id'],
                                                  'processor_id':processor_id, 'next_proc':outputs, 'uuid':UUID, 'flow_id':uuid2flowid[UUID]})
                uuid2flowid.pop(UUID)
            elif counter.counter == -1:
                for item in rollback:
                    item.delete()
                return
    for item in rollback:
        item.delete()
    # logger.info('send uuid %s' % uid.hex)
    # Channel('counter').send({'uuid': uid.hex})

def processor_runner(message):
    workflow_id = int(message['workflow_id'])
    mission_id = message['mission_id']
    processor_id = message['processor_id']
    print workflow_id
    print message['next_proc']
    cmd_header = "sudo -u spark spark-submit "

    cmd_header = cmd_header + " --class " + "Main" + ' ' + Processor.objects.get(id=processor_id).exec_file.name
    # cmd_header = cmd_header + " " + jar
    para = str(workflow_id) + "-" + str(mission_id) + "-" + str(processor_id)
    cmd_header = cmd_header + " " + para

    print cmd_header
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
        with open("/home/spark/Log/"+para, 'a') as f:
            f.write(line)
    proc.wait()

    # mot = monitor.SparkMonitor('10.5.0.223', '8088')
    # ret = mot.appInfo(app_ID)
    # appinfo = mot.byteify(json.loads(ret[2]))
    # if appinfo['app']['finalStatus'] == 'SUCCESSED':
    if 1:
        for UUID in message['next_proc']:
            counter = Counter.objects.get(guid=UUID)
            counter.counter = counter.counter + 1
            counter.save()
        update_status(workflow_id, int(message['flow_id']), 3)

    else:
        counter = Counter.objects.get(guid=message['uuid'])
        counter.counter = -1
        counter.save()

        update_status(workflow_id, int(message['flow_id']), 2)



def update_status(workflow_id, flow_id, stat):
    workflow = Workflow.objects.get(id=workflow_id)
    processor = workflow.processors.get(flow_id=int(flow_id))
    status = ConfiguredProcesserStatus.objects.get_or_create(targetWorkflow=workflow, targetProcessor=processor)
    status[0].status = stat
    status[0].save()

def ws_connect(message):
    print message.content
    with open("/home/spark/Log/"+message.content['query_string'].split('=')[1], 'r') as f:
        for line in f.readlines():
            time.sleep(1)
            message.reply_channel.send({
                "text": line,
            })


def ws_receive(message):
    print message.content
    message.reply_channel.send({
        "text": "lalala",
    })
    # print "-----------------------------"
    # with open("/home/spark/Log/2-42-13", 'r') as f:
    #     for line in f.readlines():
    #         message.reply_channel.send({
    #             "text": line
    #         })

def ws_disconnect(message):
    message.reply_channel.send({
        "text": "OK"
    })