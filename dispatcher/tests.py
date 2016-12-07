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
            'name': 'DataIO',
            'parameters': [

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
            'category': 'root1>child1>child2'
        }

workflow = {
            'name': 'simple_workflow_post_test',
            'processors': [
                {
                    'id': 13,
                    'flow_id': 1,
                    'parameters': {
                    },
                },
                {
                    'id': 12,
                    'flow_id': 2,
                    'parameters': {
                        'label1': 'test',
                        'whatever': 'A',
                    }
                }
            ],
            'connections': [
                {
                    'from': {
                        'flow_id': 1,
                        'processor_id': 13,
                        'id': 18,
                    },
                    'to': {
                        'processor_id': 12,
                        'flow_id': 2,
                        'id': 9,
                    },
                }
            ]
        }

# Processor.create_from_json_dict(processor1)
Workflow.create_from_json_dict(workflow)