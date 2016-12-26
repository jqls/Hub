# coding=utf-8
import os

from django.test import TestCase
from django.urls import reverse
import json
from workflow.models import Processor, Workflow


a = open("/root/hub/README.md")

processor2 = {
            'name': 'DataNorm',
            'parameters': [
                {
                    'label': 'label1',
                    'parameterType': 'text'
                },
                {
                    'label': 'whatever',
                    'parameterType': 'selection',
                    'choices': [
                        'A',
                        'B',
                        'C'
                    ]
                }

            ],
            'inputs': [
                {
                    'name': 'input',
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                },
                {
                    'name': 'output2',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': 'root1>child1>child3'
        }

processor1 = {
            'name': 'Document-test',
            'parameters': [
                {
                    'label': 'filePath',
                    'parameterType': 'filelist'
                },

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
            'category': 'root1>test1'
        }

processor3 = {
            'name': 'KcupNormal',
            'parameters': [

            ],
            'inputs': [
                {
                    'name': "input1",
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': 'root1>test2'
        }

processor4 = {
            'name': 'NaiveBayes',
            'parameters': [
                {
                    'label': 'lambda',
                    'parameterType': 'text'
                },
                {
                    'label': 'modelType',
                    'parameterType': 'selection',
                    'choices': [
                        'multinomial',
                        'bernoulli',
                    ]
                },
            ],
            'inputs': [
                {
                    'name': "input1",
                    'dataType': 1,
                },
                {
                    'name': "input2",
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': 'root1>test3'
        }

processor5 = {
            'name': 'Pcap',
            'parameters': [

            ],
            'inputs': [
                {
                    'name': "input1",
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': 'root1>test4'
        }

processor6 = {
            'name': 'Visualization',
            'parameters': [

            ],
            'inputs': [
                {
                    'name': "input1",
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': 'output1',
                    'dataType': 1,
                }
            ],
            'execFile': None,
            'category': 'root1>test4'
        }

workflow = {
            'name': 'simple_workflow_test',
            'processors': [
                {
                    'id': 28,
                    'flow_id': 1,
                    'parameters': {
                        "filePath": '/user/spark/DATA/kddcup.data.corrected'
                    },
                },
                {
                    'id': 29,
                    'flow_id': 2,
                    'parameters': {
                    }
                },
                {
                    'id': 28,
                    'flow_id': 6,
                    'parameters': {
                        "filePath": '/user/spark/DATA/kddcup.data_10_percent_corrected'
                    },
                },
                {
                    'id': 29,
                    'flow_id': 7,
                    'parameters': {
                    }
                },
                {
                    'id': 30,
                    'flow_id': 5,
                    'parameters': {
                        "lambda": '1.0',
                        "modelType": 'multinomial',
                    },
                },
                {
                    'id': 32,
                    'flow_id': 8,
                    'parameters': {
                    },
                },
            ],
            'connections': [
                {
                    'from': {
                        'flow_id': 1,
                        'processor_id': 28,
                        'id': 28,
                    },
                    'to': {
                        'processor_id': 29,
                        'flow_id': 2,
                        'id': 18,
                    },
                },
                {
                    'from': {
                        'flow_id': 6,
                        'processor_id': 28,
                        'id': 28,
                    },
                    'to': {
                        'processor_id': 29,
                        'flow_id': 7,
                        'id': 18,
                    },
                },
                {
                    'from': {
                        'flow_id': 2,
                        'processor_id': 29,
                        'id': 29,
                    },
                    'to': {
                        'processor_id': 30,
                        'flow_id': 5,
                        'id': 19,
                    },
                },
                {
                    'from': {
                        'flow_id': 7,
                        'processor_id': 29,
                        'id': 29,
                    },
                    'to': {
                        'processor_id': 30,
                        'flow_id': 5,
                        'id': 20,
                    },
                },
                {
                    'from': {
                        'flow_id': 5,
                        'processor_id': 30,
                        'id': 30,
                    },
                    'to': {
                        'processor_id': 32,
                        'flow_id': 8,
                        'id': 22,
                    },
                }
            ]
        }

workflow1 = {
            'name': u'新建',
            'processors': [
                {
                    'id': 28,
                    'flow_id': 1,
                    'parameters': {
                        "filePath": '/user/spark/DATA/inside.tcpdump'
                    },
                },
                {
                    'id': 31,
                    'flow_id': 2,
                    'parameters': {
                    }
                },
            ],
            'connections': [
                {
                    'from': {
                        'flow_id': 1,
                        'processor_id': 28,
                        'id': 28,
                    },
                    'to': {
                        'processor_id': 31,
                        'flow_id': 2,
                        'id': 21,
                    },
                },
            ]
        }

# Processor.create_from_json_dict(processor1)
# # Workflow.create_from_json_dict(workflow)
# # for i in range(15,24):
#     Workflow.objects.get(id=i).delete()

Processor.objects.get(id=12).delete()