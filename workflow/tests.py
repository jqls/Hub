# coding=utf-8
import json
import os

from django.test import TestCase
from django.urls import reverse
from os import path

from workflow.models.basic import DataType


def read_json(file_path):
    with open(file_path) as json_file:
        json_data = json_file.read()
    return json_data


class PostProcessorTestCase(TestCase):
    json_info = {
        'name': 'simple_post_test',
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
        DataType(type_name='Any', slug='any').save()

    def test_simple_post(self):
        exec_file_path = path.abspath(path.join(path.dirname(__file__), './examples/a.jar'))
        with open(exec_file_path) as exec_file:
            post_data = {
                'info': json.dumps(self.json_info),
                'execFile': exec_file,
            }
            response = self.client.post(reverse('workflow:processor'), data=post_data)
            self.assertEqual(response.status_code, 200, msg=response.content)

            response = self.client.get(reverse('workflow:processor'))
            print 'response of all processor: `%s`' % response.content
