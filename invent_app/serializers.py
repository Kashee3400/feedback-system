from rest_framework import serializers
from .models import *


class OTPTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPToken
        fields = '__all__'


class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmation
        fields = '__all__'


class ProfileUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    name = serializers.CharField(max_length=200, required=True)
    email = serializers.CharField(max_length=200, required=True)
    age = serializers.IntegerField(required=True)
    profile_image = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserProfileIdSerializer(serializers.Serializer):
    user_profile_id = serializers.IntegerField()
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_code', 'role']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['mcc', 'mcc_code']


class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocations
        fields = ['mpp_loc', 'mpp_loc_code']


# class FarmerFeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FarmerFeedback
#         fields = '__all__'

import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import FarmerFeedback, FarmerFeedbackFile

class Base64FileField(serializers.FileField):
    """
    A custom file field to handle base64 encoded files.
    """
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                decoded_file = base64.b64decode(data)
                return ContentFile(decoded_file, name='uploaded_file')
            except Exception as e:
                raise serializers.ValidationError(f'Invalid base64 format: {e}')
        else:
            return super().to_internal_value(data)

class FeedbackFileSerializer(serializers.Serializer):
    file = Base64FileField()

    def create(self, validated_data):
        return validated_data

class FarmerFeedbackSerializer(serializers.ModelSerializer):
    files = FeedbackFileSerializer(many=True, required=False)

    class Meta:
        model = FarmerFeedback
        fields = '__all__'

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        feedback = FarmerFeedback.objects.create(**validated_data)
        for file_data in files_data:
            file = file_data['file']
            FarmerFeedbackFile.objects.create(feedback=feedback, file=file)
        return feedback


class FeedbackCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackCategory
        fields = '__all__'

