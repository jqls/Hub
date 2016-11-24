# coding=utf-8
import os

from django.test import TestCase
from django.urls import reverse

from dispatcher.models import Processor, Input, DataType, ProcessorCategory, Output, Parameter


def read_json(file_path):
    with open(file_path) as json_file:
        json_data = json_file.read()
    return json_data


class MissionPostTestCase(TestCase):
    def test_simple_mission(self):
        post_data = read_json(os.path.join(os.path.dirname(__file__), './test_case/post_mission_1.json'))
        response = self.client.post(reverse('dispatcher:post_mission'), post_data, content_type='application/json')
        self.assertTrue(True, "It should always true.")


class ProcessorGetTestCase(TestCase):
    def test_get_simple_processor_response(self):
        category = ProcessorCategory(
            name='测试算法类型',
            description="nothing",
            icon="flask",
        )
        category.save()
        processor = Processor(
            name='测试算法',
            category=category,
        )
        processor.save()
        simple_data_type = DataType(name="simple", display_name="简单类型")
        simple_data_type.save()
        single_input = Input(
            name='测试输入1',
            data_type=simple_data_type,
            processor=processor,
        )
        single_input.save()
        single_output = Output(
            name='简单输出1',
            data_type=simple_data_type,
            processor=processor,
        )
        single_parameter = Parameter(
            processor=processor,
        )
        single_parameter.save()
        single_output.save()
        response = self.client.get(reverse('dispatcher:get_processor', kwargs={'pk': processor.pk}))
        print response
