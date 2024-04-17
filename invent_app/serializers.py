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
        fields = ['id', 'role']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['mcc', 'mcc_code']


class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocations
        fields = ['mpp_loc', 'mpp_loc_code']


class FarmerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerFeedback
        fields = '__all__'


from rest_framework import serializers
from .models import FeedbackCategory

class FeedbackCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackCategory
        fields = '__all__'


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        
        fields = '__all__'
