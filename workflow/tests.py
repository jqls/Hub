# coding=utf-8
import json
import os

from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from os import path

from workflow.models.basic import DataType

example_exec_file_path = path.abspath(path.join(path.dirname(__file__), './examples/a.jar'))


# todo: 测试文件有问题, DataType创建稍麻烦

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
    def get_workflow_json_info(self, proocessor1_id, processor2_id, data_type_id):
        return {
            'name': 'simple_workflow_post_test',
            'processors': [
                {
                    'id': proocessor1_id,
                    'parameters': {
                        'parameter_a': 'counter',
                        'parameter_b': 'C',
                    },
                },
                {
                    'id': processor2_id,
                    'parameters': {
                        'parameter_c': 'counter',
                    }
                }
            ],
            'connections': [
                {
                    'from': {
                        'processor_id': proocessor1_id,
                        'id': 1,
                    },
                    'to': {
                        'processor_id': processor2_id,
                        'id': 2,
                    },
                }
            ]
        }

    def get_processor1_json(self, data_type_id):
        return {
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
                    'dataType': data_type_id,
                }
            ],
            'outputs': [
                {
                    'name': '输出',
                    'dataType': data_type_id,
                }
            ]
        }

    def get_processor2_json(self, data_type_id):
        return {
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
                    'dataType': data_type_id,
                }
            ],
            'outputs': [
                {
                    'name': '输出',
                    'dataType': data_type_id,
                }
            ]
        }

    def setUp(self):
        try:
            self.data_type_id = DataType.objects.get(type_name='Any').id
        except Exception:
            data_type = DataType(type_name='Any', slug='any')
            data_type.save()
            self.data_type_id = data_type.pk

    def test_post_workflow(self):
        post_new_processor(self, self.get_processor1_json(self.data_type_id))
        post_new_processor(self, self.get_processor2_json(self.data_type_id))
        post_new_workflow(self, self.get_workflow_json_info(1, 2, self.data_type_id))
        response = self.client.get(reverse('workflow:workflow'))
        print response.content


# class PostProcessorTestCase(TestCase):
#     def get_json_info(self, data_type_id):
#         return {
#             'name': 'simple_processor_post_test',
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
#             ],
#             'inputs': [
#                 {
#                     'name': '输入',
#                     'dataType': data_type_id,
#                 }
#             ],
#             'outputs': [
#                 {
#                     'name': '输出',
#                     'dataType': data_type_id,
#                 }
#             ]
#         }
#
#     def setUp(self):
#         try:
#             self.data_type_id = DataType.objects.get(type_name='Any').id
#         except Exception:
#             data_type = DataType(type_name='Any', slug='any')
#             data_type.save()
#             self.data_type_id = data_type.pk
#
#     def test_simple_post(self):
#         response = post_new_processor(self, self.get_json_info(self.data_type_id))
#         self.assertEqual(response.status_code, 200, msg=response.content)
#
#         response = self.client.get(reverse('workflow:processor'))
#         print 'response of all processor: `%s`' % response.content
