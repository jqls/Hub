# coding=utf-8
import os

from django.test import TestCase
from django.urls import reverse
import json
from workflow.models import Processor, Workflow
#
#
# a = open("/root/hub/README.md")
#
# processor2 = {
#             'name': 'DataNorm',
#             'parameters': [
#                 {
#                     'label': 'label1',
#                     'parameterType': 'text'
#                 },
#                 {
#                     'label': 'whatever',
#                     'parameterType': 'selection',
#                     'choices': [
#                         'A',
#                         'B',
#                         'C'
#                     ]
#                 }
#
#             ],
#             'inputs': [
#                 {
#                     'name': 'input',
#                     'dataType': 1,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 },
#                 {
#                     'name': 'output2',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>child1>child3'
#         }
#
# processor1 = {
#             'name': 'Document-test',
#             'parameters': [
#                 {
#                     'label': 'filePath',
#                     'parameterType': 'filelist'
#                 },
#
#             ],
#             'inputs': [
#
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>test1'
#         }
#
# processor3 = {
#             'name': 'KcupNormal',
#             'parameters': [
#
#             ],
#             'inputs': [
#                 {
#                     'name': "input1",
#                     'dataType': 1,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>test2'
#         }
#
# processor4 = {
#             'name': 'NaiveBayes',
#             'parameters': [
#                 {
#                     'label': 'lambda',
#                     'parameterType': 'text'
#                 },
#                 {
#                     'label': 'modelType',
#                     'parameterType': 'selection',
#                     'choices': [
#                         'multinomial',
#                         'bernoulli',
#                     ]
#                 },
#             ],
#             'inputs': [
#                 {
#                     'name': "input1",
#                     'dataType': 1,
#                 },
#                 {
#                     'name': "input2",
#                     'dataType': 1,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>test3'
#         }
#
# processor5 = {
#             'name': 'Pcap',
#             'parameters': [
#
#             ],
#             'inputs': [
#                 {
#                     'name': "input1",
#                     'dataType': 1,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>test4'
#         }
#
# processor6 = {
#             'name': 'Visualization',
#             'parameters': [
#
#             ],
#             'inputs': [
#                 {
#                     'name': "input1",
#                     'dataType': 1,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': 'output1',
#                     'dataType': 1,
#                 }
#             ],
#             'execFile': None,
#             'category': 'root1>test4'
#         }
#
# workflow = {
#             'name': 'simple_workflow_test',
#             'processors': [
#                 {
#                     'id': 28,
#                     'flow_id': 1,
#                     'parameters': {
#                         "filePath": '/user/spark/DATA/kddcup.data.corrected'
#                     },
#                 },
#                 {
#                     'id': 29,
#                     'flow_id': 2,
#                     'parameters': {
#                     }
#                 },
#                 {
#                     'id': 28,
#                     'flow_id': 6,
#                     'parameters': {
#                         "filePath": '/user/spark/DATA/kddcup.data_10_percent_corrected'
#                     },
#                 },
#                 {
#                     'id': 29,
#                     'flow_id': 7,
#                     'parameters': {
#                     }
#                 },
#                 {
#                     'id': 30,
#                     'flow_id': 5,
#                     'parameters': {
#                         "lambda": '1.0',
#                         "modelType": 'multinomial',
#                     },
#                 },
#                 {
#                     'id': 32,
#                     'flow_id': 8,
#                     'parameters': {
#                     },
#                 },
#             ],
#             'connections': [
#                 {
#                     'from': {
#                         'flow_id': 1,
#                         'processor_id': 28,
#                         'id': 28,
#                     },
#                     'to': {
#                         'processor_id': 29,
#                         'flow_id': 2,
#                         'id': 18,
#                     },
#                 },
#                 {
#                     'from': {
#                         'flow_id': 6,
#                         'processor_id': 28,
#                         'id': 28,
#                     },
#                     'to': {
#                         'processor_id': 29,
#                         'flow_id': 7,
#                         'id': 18,
#                     },
#                 },
#                 {
#                     'from': {
#                         'flow_id': 2,
#                         'processor_id': 29,
#                         'id': 29,
#                     },
#                     'to': {
#                         'processor_id': 30,
#                         'flow_id': 5,
#                         'id': 19,
#                     },
#                 },
#                 {
#                     'from': {
#                         'flow_id': 7,
#                         'processor_id': 29,
#                         'id': 29,
#                     },
#                     'to': {
#                         'processor_id': 30,
#                         'flow_id': 5,
#                         'id': 20,
#                     },
#                 },
#                 {
#                     'from': {
#                         'flow_id': 5,
#                         'processor_id': 30,
#                         'id': 30,
#                     },
#                     'to': {
#                         'processor_id': 32,
#                         'flow_id': 8,
#                         'id': 22,
#                     },
#                 }
#             ]
#         }
#
# workflow1 = {
#             'name': u'新建',
#             'processors': [
#                 {
#                     'id': 28,
#                     'flow_id': 1,
#                     'parameters': {
#                         "filePath": '/user/spark/DATA/inside.tcpdump'
#                     },
#                 },
#                 {
#                     'id': 31,
#                     'flow_id': 2,
#                     'parameters': {
#                     }
#                 },
#             ],
#             'connections': [
#                 {
#                     'from': {
#                         'flow_id': 1,
#                         'processor_id': 28,
#                         'id': 28,
#                     },
#                     'to': {
#                         'processor_id': 31,
#                         'flow_id': 2,
#                         'id': 21,
#                     },
#                 },
#             ]
#         }
#
# # Processor.create_from_json_dict(processor1)
# # # Workflow.create_from_json_dict(workflow)
# for i in range(8,9):
#     Workflow.objects.get(id=i).delete()
#
# # Processor.objects.get(id=12).delete()

processor1 = {
            'name': 'SQL',
            'ac_id': '1',
            'is_visualization': 0,
            'parameters': [
                {
                    'label': 'sql_list',
                    'parameterType': 'database'
                },
                {
                    'label': 'host',
                    'parameterType': 'text',
                    'belong_to': 'mysql',
                    'stage': 1
                },
                {
                    'label': 'port',
                    'parameterType': 'text',
                    'belong_to': 'mysql',
                    'stage': 1
                },
                {
                    'label': 'user',
                    'parameterType': 'text',
                    'belong_to': 'mysql',
                    'stage': 1
                },
                {
                    'label': 'password',
                    'parameterType': 'text',
                    'belong_to': 'mysql',
                    'stage': 1
                },
                {
                    'label': 'dbase',
                    'parameterType': 'text',
                    'belong_to': 'mysql',
                    'stage': 1
                },
                {
                    'label': 'tablelist',
                    'parameterType': 'selection',
                    'choices': [],
                    'belong_to': 'mysql',
                    'stage': 2
                },
                {
                    'label': 'columnlist',
                    'parameterType': 'selection',
                    'choices': [],
                    'belong_to': 'mysql',
                    'stage': 3
                }

            ],
            'inputs': [

            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': '-1>6'
        }

workflow1 = {
            'name': 'test-sql',
            'processors': [
                {
                    'id': 28,
                    'flow_id': 1,
                    'parameters': {
                        "sql_list": 'mysql',
                        "host": '10.5.0.224',
                        "port": "3306",
                        "user": "root",
                        "password": "asd123",
                        "dbase": "dispatcher_dev",
                        "tablelist": "workflow_database",
                        "columnlist": "id,db_id",
                    },
                    "loc_x": 0,
                    "loc_y": 0,
                },
            ],
            'connections': [
            ]
        }
# Processor.create_from_json_dict(processor1)
Workflow.create_from_json_dict(workflow1)
# Processor.objects.get(id=27).delete()
# import httplib
# import json
#
# path = "/workflow/sql/1/"
# headers = {
#             'Accept': 'application/json'
#         }
# data = {"ac_id":1, "db_id":1, "parameters":{"host":"10.5.0.224", "port":"3306", "user":"root", "password":"asd123", "dbase":"dispatcher_dev", "table_name":"workflow_document"}}
# conn = httplib.HTTPConnection("10.5.0.222", "8080")
# conn.request("POST", path, json.dumps(data), headers)
# response = conn.getresponse()
# ret = (response.status, response.reason, response.read())
# conn.close()
# print ret