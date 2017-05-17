from dispatcher.models import Mission, Workflow
from rest_framework import serializers

class MissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mission
        fields = ("id", "startDate", "endDate", "status")