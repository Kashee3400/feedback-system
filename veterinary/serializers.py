from rest_framework import serializers
from .models import *


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        
        fields = '__all__'


class TAGTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TAGType
        fields = '__all__'


class CattleCaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CattleCaseType
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'
        

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class DiagnosisRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisRoute
        fields = '__all__'

class SymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptoms
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms = SymptomsSerializer(many=True)
    class Meta:
        model = Disease
        fields = '__all__'

class CattleTaggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CattleTagging
        fields = '__all__'