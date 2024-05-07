# serializers.py
from rest_framework import serializers
from .models import *
from vcg.serializers import FilterVMPPsSerializer

class AwarenessTeamMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwarenessTeamMembers
        fields = '__all__'


class AwarenessSerializer(serializers.ModelSerializer):
    awareness_team = AwarenessTeamMembersSerializer(many=True, read_only=True)
    mpp_awareness = FilterVMPPsSerializer(source='mpp')

    class Meta:
        model = Awareness
        fields = '__all__'
