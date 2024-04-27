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


# serializers.py
from rest_framework import serializers
from .models import VMCCs

class VMCCsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMCCs
        fields = ['mcc', 'mcc_code', 'created_at']


# serializers.py
from rest_framework import serializers
from .models import VMPPs

class VMPPsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMPPs
        fields = ['mcc', 'mpp_loc', 'mpp_loc_code', 'district', 'created_at']
        read_only_fields = ['mcc']  # Make mcc read-only

# serializers.py
from rest_framework import serializers
from .models import VMPPs

class VMPPsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMPPs
        fields = ['mcc', 'mpp_loc', 'mpp_loc_code', 'district', 'created_at']

# serializers.py
from rest_framework import serializers
from .models import VMPPs

class FilterVMPPsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMPPs
        fields = ['mcc', 'mpp_loc', 'mpp_loc_code', 'district', 'created_at']
        read_only_fields = ['mcc']  # Make mcc read-only



class VCGroupSerializer(serializers.ModelSerializer):
    member_code = serializers.CharField(source='member.code')
    member_name = serializers.CharField(source='member.name')
    whatsapp_number = serializers.CharField(source='whatsapp_num')

    class Meta:
        model = VCGroup
        fields = ('member_code', 'member_name', 'whatsapp_number')


from rest_framework import serializers
from .models import ConductedByType

class ConductedByTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConductedByType
        fields = '__all__'


class FacilitatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        fields = ['id','name']


class ConductedByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConductedByName
        fields = ['id','name']
        
        
class VMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMembers
        fields = '__all__'

class ZeroDaysReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZeroDaysPourerReason
        fields = '__all__'

class MemberComplaintReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCompaintReason
        fields = '__all__'



class VCGMeetingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VCGMeetingImages
        fields = '__all__'

class MonthAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthAssignment
        fields = '__all__'
