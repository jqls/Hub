# coding=utf-8
import os

from django.test import TestCase
from django.urls import reverse
import json
from workflow.models import Processor


a = open("/root/hub/README.md")

processor = {
            'name': 'Data_IO',
            'parameters': [

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
            ],
            'execFile': a
        }

Processor.create_from_json_dict(processor)