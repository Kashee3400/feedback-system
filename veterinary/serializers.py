from rest_framework import serializers
from .models import *


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        
        fields = '__all__'
