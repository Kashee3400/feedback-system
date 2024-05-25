from django.shortcuts import render
from .models import *
from .serializers import *
from datetime import datetime
import base64
from django.core.files.base import ContentFile
import random
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Count
from rest_framework.permissions import AllowAny


class VMCCsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = VMCCs.objects.all()
    serializer_class = VMCCsSerializer

class VMPPsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = VMPPs.objects.all()
    serializer_class = VMPPsSerializer


class FilterVMPPsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = VMPPs.objects.all()
    serializer_class = FilterVMPPsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mcc_code = self.request.query_params.get('mcc_code')
        if mcc_code:
            queryset = queryset.filter(mcc_id=mcc_code)
        return queryset


from rest_framework import generics

class VCGroupListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VCGroupSerializer

    def get_queryset(self):
        mpp_id = self.request.data.get('mpp')
        members = VMembers.objects.filter(mpp_id=mpp_id)
        groups = VCGroup.objects.filter(member__in=members)
        return groups

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class MarkVCGMemberAttendance(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        member_codes = request.data.get('member_codes', [])
        meeting_id = request.data.get('meeting_id')
        status_code = status.HTTP_200_OK 
        for member_code in member_codes:
            try:
                meeting=VCGMeeting.objects.get(meeting_id=meeting_id)
                member = VMembers.objects.get(code=member_code)
                vcg_group_mem = VCGroup.objects.get(member=member)
                if VCGMemberAttendance.objects.filter(member=vcg_group_mem,meeting = meeting).exists():
                    attendance = VCGMemberAttendance.objects.get(member=vcg_group_mem,meeting = meeting)
                    attendance.status = "present"
                    attendance.save()
                else: 
                    attendance = VCGMemberAttendance.objects.create(member=vcg_group_mem, status="present",meeting = meeting)
            except VMembers.DoesNotExist:
                return Response({'message': f'Member with code {member_code} not found'}, status=status.HTTP_404_NOT_FOUND)
            except VCGroup.DoesNotExist:
                # Handle case where VCGroup for member doesn't exist
                return Response({'message': f'VCGroup for member with code {member_code} not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                # Handle other exceptions
                print(e)
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Attendance Marked Successfully'}, status=status_code)

class ZeroDaysReasonReport(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        status_code = status.HTTP_200_OK
        meeting_id = data['meeting_id']
        member_id = data['member_id']
        reason_id = data['reason_id']
        vmember = VMembers.objects.get(id=member_id)
        reason = ZeroDaysPourerReason.objects.get(id=reason_id)
        meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
        if ZeroDaysPouringReport.objects.filter(meeting=meeting,member=vmember).exists():
           report =  ZeroDaysPouringReport.objects.get(meeting=meeting,member=vmember)
           report.reason = reason
           report.save()
        else:
            report = ZeroDaysPouringReport.objects.create(member_id=member_id,reason_id=reason_id,meeting=meeting)
        response = {
                'message': 'Submitted Successfully',
                'name':report.member.name,
                'code':report.member.code,
                'meeting':report.meeting.meeting_id
                
            }
        return Response(response, status=status_code)

class MonthAssignmentAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        status_code = status.HTTP_200_OK
        mpp_code = data['mpp_id']
        try:
            mpp = VMPPs.objects.get(pk=mpp_code)
            month_asgmnt = MonthAssignment.objects.get(mpp=mpp)
            asgnmnt_serializer = MonthAssignmentSerializer(month_asgmnt)
            members = VMembers.objects.filter(mpp_id=mpp_code)
            max_pouring_member = members.order_by('-max_qty')[:2]
            mnrl_mxr_member = members.filter(mpp_id=mpp_code,mineral_bag__gt=0).order_by('-mineral_bag')
            cattle_feed_member = members.filter(mpp_id=mpp_code,cattle_bag__gt=0).order_by('-cattle_bag')
            response_data = asgnmnt_serializer.data
            member_serializer = VMembersSerializer(max_pouring_member, many=True)
            cattle_feed_member_serializer = VMembersSerializer(cattle_feed_member, many=True)
            mnrl_mxr_member_serializer = VMembersSerializer(mnrl_mxr_member, many=True)
            max_pouring_member_data = member_serializer.data
            cattle_feed_member_data = cattle_feed_member_serializer.data
            mnrl_mxr_member_data = mnrl_mxr_member_serializer.data
            response = {
                'message': 'Submitted Successfully',
                'data': response_data,
                'max_pouring_member':max_pouring_member_data,
                'cattle_feed':cattle_feed_member_data,
                'mineral_mixture':mnrl_mxr_member_data,
            }
            return Response(response, status=status_code)
        except VMPPs.DoesNotExist:
            return Response({'message': 'VMPP with the provided ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except MonthAssignment.DoesNotExist:
            return Response({'message': 'MonthAssignment for the provided VMPP ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

class ComplaintReport(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        status_code = status.HTTP_200_OK
        meeting_id = data['meeting_id']
        member_id = data['member_id']
        reason_id = data['reason_id']
        vmember = VMembers.objects.get(id=member_id)
        reason = MemberCompaintReason.objects.get(id=reason_id)
        meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
        if MemberComplaintReport.objects.filter(meeting=meeting,member=vmember).exists():
           report =  MemberComplaintReport.objects.get(meeting=meeting,member=vmember)
           report.reason = reason
           report.save()
        else:
            report = MemberComplaintReport.objects.create(member_id=member_id,reason_id=reason_id,meeting=meeting)
        response = {
                'message': 'Submitted Successfully',
                'name':report.member.name,
                'code':report.member.code,
                'meeting':report.meeting.meeting_id
                
            }
        return Response(response, status=status_code)


from django.db.utils import IntegrityError

class StartMeetingAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        data = request.data
        status_code = status.HTTP_200_OK
        try:
            mpp_id = data['mpp_id']
            type = data['type']
            meeting_id = data['meeting_id']
            type_id = data['type_id']
            conducted_by_name_id = data['conducted_by_name_id']
            date_time = data['date_time']
            date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')
            facilitator = None
            conducted_by_name = None
            mpp = VMPPs.objects.get(mpp_loc_code=mpp_id)
            c_type = ConductedByType.objects.get(id=type_id)

            if VCGMeeting.objects.filter(meeting_id=meeting_id).exists():
                meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
                if meeting.status == VCGMeeting.COMPLETED:
                    return Response({'message': 'Meeting Already Conducted'}, status=status.HTTP_400_BAD_REQUEST)
                meeting.mpp = mpp
                meeting.conducted_by_type = c_type
                meeting.start_datetime = date_time_obj
                if type == 'Facilitator':
                    facilitator = Facilitator.objects.get(id=conducted_by_name_id)
                    meeting.conducted_by_fs = facilitator
                    meeting.conducted_by_name = None
                else:
                    conducted_by_name = ConductedByName.objects.get(id=conducted_by_name_id)
                    meeting.conducted_by_fs = None
                meeting.save()
                response = {
                    'message': f'{meeting.meeting_id} created successfully',
                    'meeting_id': meeting.meeting_id
                }
            else:
                if type == 'Facilitator':
                    facilitator = Facilitator.objects.get(id=conducted_by_name_id)
                else:
                    conducted_by_name = ConductedByName.objects.get(id=conducted_by_name_id)
                
                meeting = VCGMeeting.objects.create(
                    mpp=mpp,
                    conducted_by_type=c_type,
                    conducted_by_fs=facilitator,
                    conducted_by_name=conducted_by_name,
                    start_datetime=date_time_obj,
                )
                response = {
                    'message': f'{meeting.meeting_id} created successfully',
                    'meeting_id': meeting.meeting_id
                }

        except IntegrityError:
            response = {
                'message': 'Meeting Already Exists'
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)

class ConductedByTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ConductedByType.objects.all()
    serializer_class = ConductedByTypeSerializer

class ZeroDaysReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ZeroDaysPourerReason.objects.all()
    serializer_class = ZeroDaysReasonSerializer

class MemberComplaintReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MemberCompaintReason.objects.all()
    serializer_class = MemberComplaintReasonSerializer


class FacilitatorListView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Facilitator.objects.all()
    serializer_class = FacilitatorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mcc_code = self.request.query_params.get('mcc_code')
        if mcc_code:
            queryset = queryset.filter(mcc_id=mcc_code)
        return queryset

class ConductedByNmeListView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ConductedByName.objects.all()
    serializer_class = ConductedByNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.query_params.get('type_id')
        if type:
            queryset = queryset.filter(type_id=type_id)
        return queryset


class VMembersMobileViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = VMembersSerializer

    def list(self, request):
        mpp_id = request.query_params.get('mpp_id')
        max_qty = request.query_params.get('max_qty')
        if mpp_id is not None:
            queryset = self.get_queryset(mpp_id,max_qty)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "mpp_id parameter is required."}, status=400)

    def get_queryset(self, mpp_id,max_qty):
        if max_qty:  
            queryset = VMembers.objects.filter(mpp_id=mpp_id, max_qty=0)
        else:
            queryset = VMembers.objects.filter(mpp_id=mpp_id)
        return queryset


class EndMeetingAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        if 'images' in request.data:
            base64_images = request.data.get('images')
            meeting_id = request.data.get('meeting_id')
            selected_datetime = request.data.get('date_time')
            meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
            for base64_image in base64_images:
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f"{random.randint(100, 999)}_{meeting_id}_{selected_datetime}.jpg")
                meeting_image = VCGMeetingImages.objects.create(
                    meeting=meeting,
                    image=image_file,
                )
            meeting.end_datetime = selected_datetime
            meeting.status = VCGMeeting.COMPLETED
            meeting.save()
            response = {
                'message': 'Images uploaded successfully',
                'meeting_id': meeting.meeting_id
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No files were uploaded"}, status=status.HTTP_400_BAD_REQUEST)


class UserAuthentication(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({'message': 'Authentication successful'})
        else:
            return Response({'message': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

class ZeroDaysPouringReportList(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        if meeting_id:
            try:
                meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
                z_reports = ZeroDaysPouringReport.objects.filter(meeting=meeting)
                list_data = []
                for z_report in z_reports:
                    response_data = {
                        "name":z_report.member.name,
                        "code":z_report.member.code,
                        'reason':z_report.reason.reason,
                        "mpp":z_report.member.mpp.mpp_loc,
                        'mpp_code':z_report.member.mpp.mpp_loc_code,
                    }
                    list_data.append(response_data)
                return Response({'data': list_data})
            except VCGMeeting.DoesNotExist:
                return Response({'message': 'Meeting with the specified ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Meeting ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

class MemberComplaintReportList(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        if meeting_id:
            try:
                meeting = VCGMeeting.objects.get(meeting_id=meeting_id)
                c_reports = MemberComplaintReport.objects.filter(meeting=meeting)
                list_data = []
                for c_report in c_reports:
                    response_data = {
                        "name":c_report.member.name,
                        "code":c_report.member.code,
                        'reason':c_report.reason.reason,
                        "mpp":c_report.member.mpp.mpp_loc,
                        'mpp_code':c_report.member.mpp.mpp_loc_code,
                    }
                    list_data.append(response_data)
                return Response({'data': list_data})
            except VCGMeeting.DoesNotExist:
                return Response({'message': 'Meeting with the specified ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Meeting ID not provided'}, status=status.HTTP_400_BAD_REQUEST)


class VCGMeetingListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = VCGMeetingSerializer

    def get_queryset(self):
        # queryset = VCGMeeting.objects.all()
        queryset = VCGMeeting.objects.annotate(num_images=Count('meeting_images'))
        # return queryset
        return queryset.filter(num_images=0)