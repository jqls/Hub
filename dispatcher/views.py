# coding=utf-8
import json

from channels.channel import Channel
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from models import Mission, Workflow
from datetime import datetime


def submit_mission_view(request):
    info = ''
    try:
        if request.method == 'POST':
            startdate = datetime.now()
            mission = Mission(status=0, missionStartDate=startdate,
                              missionEndDate=datetime.now(),workflow=Workflow.objects.get(id=str(request.POST["workflow_id"])))
            mission.save()
            missionId = str(Mission.objects.get(startDate=startdate).id)
            Channel('submit_mission').send({'workflow_id':request.POST["workflow_id"], 'mission_id': missionId})

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    return HttpResponse()
