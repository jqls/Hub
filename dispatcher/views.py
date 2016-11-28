# coding=utf-8
import json

from channels.channel import Channel
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404


def submit_mission_view(request):
    Channel('submit_mission').send({'mission_id': 1})
    return HttpResponse()
