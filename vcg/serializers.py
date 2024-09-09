# serializers.py
from rest_framework import serializers
from .models import *

class VMCCsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMCCs
        fields = ['mcc', 'mcc_code', 'created_at']


class VMPPsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VMPPs
        fields = ['mcc', 'mpp_loc', 'mpp_loc_code', 'district', 'created_at']


class FilterVMPPsSerializer(serializers.ModelSerializer):
    mcc_meeting = VMCCsSerializer(source='mcc')
    class Meta:
        model = VMPPs
        fields = ['mcc_meeting', 'mpp_loc', 'mpp_loc_code', 'district', 'created_at']
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
        fields = ['id','conducted_type']


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


class VCGMemeberAttendanceSerializer(serializers.ModelSerializer):
    member = VCGroupSerializer()
    class Meta:
        model = VCGMemberAttendance
        fields =['member','status','date']


class ZeroDaysPouringReportSerializer(serializers.ModelSerializer):
    reason = ZeroDaysReasonSerializer()
    member = VMembersSerializer()
    class Meta:
        model = ZeroDaysPouringReport
        fields = ['member', 'reason']
        
class MemberComplaintReportSerializer(serializers.ModelSerializer):
    reason = MemberComplaintReasonSerializer()
    member = VMembersSerializer()
    class Meta:
        model = MemberComplaintReport
        fields = ['member', 'reason']


class VCGMeetingSerializer(serializers.ModelSerializer):
    conducted_by_type = ConductedByTypeSerializer()
    conducted_by_name = ConductedByNameSerializer()
    conducted_by_fs = FacilitatorSerializer()
    mpp_meeting = FilterVMPPsSerializer(source='mpp')
    attendances = VCGMemeberAttendanceSerializer(many=True, read_only=True)
    meeting_zero_days_pouring = ZeroDaysPouringReportSerializer(many=True, read_only=True)
    meeting_member_complaints = MemberComplaintReportSerializer(many=True, read_only=True)
    class Meta:
        model = VCGMeeting
        fields = ['meeting_id','mpp_meeting', 'conducted_by_type', 'conducted_by_name', 'conducted_by_fs', 'start_datetime', 'end_datetime', 'status', 'attendances','meeting_zero_days_pouring','meeting_member_complaints']


class ZeroPourerMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZeroPourerMembers
        fields = ['id', 'name']  # Include any fields you need
