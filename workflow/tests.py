# coding=utf-8
import json
import os

from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from os import path

from workflow.models.basic import DataType

example_exec_file_path = path.abspath(path.join(path.dirname(__file__), './examples/a.jar'))


def read_json(file_path):
    with open(file_path) as json_file:
        json_data = json_file.read()
    return json_data


def __post_new(test_case, url, content_type=MULTIPART_CONTENT):
    def post_new_with(attribute_json):
        response = test_case.client.post(
            url,
            data=attribute_json,
            content_type=content_type,
        )
        print '%s response content is `%s`, status code is %d' % (url, response.content, response.status_code)
        test_case.assertEqual(response.status_code, 200, msg=response.content)
        return response

    return post_new_with


def post_new_processor(test_case, attributes_json):
    with open(example_exec_file_path) as exec_file:
        post_data = {
            'info': json.dumps(attributes_json),
            'execFile': exec_file,
        }
        return __post_new(test_case, reverse('workflow:processor'))(post_data)


def post_new_workflow(test_case, attributes_json):
    return __post_new(
        test_case,
        reverse('workflow:workflow'),
        content_type='application/json')(json.dumps(attributes_json))


class PostWorkflowTestCase(TestCase):
    workflow_json_info = {
        'name': 'simple_workflow_post_test',
        'processors': [
            {
                'id': 1,
                'parameters': {
                    'parameter_a': 'counter',
                    'parameter_b': 'C',
                },
            },
            {
                'id': 2,
                'parameters': {
                    'parameter_c': 'counter',
                }
            }
        ],
        'connections': [
            {
                'from': {
                    'processor_id': 1,
                    'id': 1,
                },
                'to': {
                    'processor_id': 2,
                    'id': 2,
                },
            }
        ]
    }

    processor1_json = {
        'name': 'processor_input',
        'parameters': [
            {
                'label': 'parameter_a',
                'parameterType': 'text'
            },
            {
                'label': 'parameter_b',
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
                'name': '输入',
                'dataType': 1,
            }
        ],
        'outputs': [
            {
                'name': '输出',
                'dataType': 1,
            }
        ]
    }

    processor2_json = {
        'name': 'processor_output',
        'parameters': [
            {
                'label': 'parameter_c',
                'parameterType': 'text'
            },
        ],
        'inputs': [
            {
                'name': '输入',
                'dataType': 1,
            }
        ],
        'outputs': [
            {
                'name': '输出',
                'dataType': 1,
            }
        ]
    }

    def setUp(self):
        try:
            DataType.objects.get(type_name='Any')
        except Exception:
            DataType(type_name='Any', slug='any').save()

    def test_post_workflow(self):
        post_new_processor(self, self.processor1_json)
        post_new_processor(self, self.processor2_json)
        post_new_workflow(self, self.workflow_json_info)
        response = self.client.get(reverse('workflow:workflow'))
        print response.content

    class PostProcessorTestCase(TestCase):
        json_info = {
            'name': 'simple_processor_post_test',
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
                    'name': '输入',
                    'dataType': 1,
                }
            ],
            'outputs': [
                {
                    'name': '输出',
                    'dataType': 1,
                }
            ]
        }

        def setUp(self):
            try:
                DataType.objects.get(type_name='Any')
            except Exception:
                DataType(type_name='Any', slug='any').save()

        def test_simple_post(self):
            with open(example_exec_file_path) as exec_file:
                post_data = {
                    'info': json.dumps(self.json_info),
                    'execFile': exec_file,
                }

                response = post_new_processor(self, post_data)
                self.assertEqual(response.status_code, 200, msg=response.content)

                response = self.client.get(reverse('workflow:processor'))
                print 'response of all processor: `%s`' % response.content
