from rest_framework import generics, status
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.decorators import api_view
import base64
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from invent_app.serializers import *
from django.shortcuts import render, get_object_or_404
import random
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.contrib import messages
from django.utils import timezone
from invent_app.models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



def generate_otp():
    digits = "0123456789"
    return ''.join(random.choice(digits) for _ in range(6))


def create_otp(user):
    expiry_time = timezone.now() + timedelta(minutes=1)    
    # Generate the OTP token
    otp_token = generate_otp()
    # Create the OTPToken object with user, token, and expiry time
    otp_token_obj = OTPToken.objects.create(user=user, token=otp_token, expiry_time=expiry_time)
    
    return otp_token_obj

class SendOTPView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            user = ""
            if email:
                if CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.get(email=email)
                else:    
                    return JsonResponse({'message': f'User {email} not exists. Please contact admin'}, status=400)
                otp = create_otp(user)
                subject = 'Feedbacks System OTP verification'
                to_email = [email]
                logo = Logo.objects.all()
                html_content = render_to_string(
                    'api/otp_email_template.html', {'otp': otp, 'for': 'login', 'logo': logo})
                email = EmailMessage(subject, html_content,
                                     settings.EMAIL_HOST_USER, to_email)
                email.content_subtype = 'html'
                email.send()
                return JsonResponse({'message': "OTP sent successfully!!"})
            else:
                return JsonResponse({'message': 'Email is required'}, status=400)
        else:
            return JsonResponse({'response': 'error while sending the OTP'})


class EmailOTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_token = request.data.get('otp')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            if verify_otp(user, otp_token):
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                data ={'message': 'Logged in successfully', 
                       'status':200,
                       'token': token.key,
                       "user_id":user.id
                       }
                return Response(data, status=status.HTTP_200_OK)
            else:
                OTPToken.objects.all().delete()
                return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except OTPToken.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def verify_otp(user, otp):
    otp_token = OTPToken.objects.filter(
        user=user, token=otp).order_by('-created_at').last()
    if otp_token:
        time_difference = timezone.now() - otp_token.created_at
        # OTP expires after 5 minutes (300 seconds)
        if time_difference.seconds < 300:
            otp_token.delete()
            return True
    return False

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_data(request):
    try:
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get("user_id")
            profile = Profile.objects.get(user=user_id)
            if profile.profile_image:
                existing_image_path = profile.profile_image.path
                default_storage.delete(existing_image_path)
            if 'phone_number' in serializer.validated_data:
                profile.phone_number = serializer.validated_data['phone_number']
            if 'profile_image' in serializer.validated_data:
                profile_image_data = serializer.validated_data['profile_image']
                gender = serializer.validated_data['gender']
                email = serializer.validated_data['email']
                name = serializer.validated_data['name']
                try:
                    user = CustomUser.objects.get(email=email)
                    if user.id != user_id:
                        return Response({"message": "Email is already associated with another user."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user.first_name = name
                        user.save()

                except CustomUser.DoesNotExist:
                    user = CustomUser.objects.get(pk=user_id)
                    user.username = email
                    user.email = email
                    user.first_name = name
                    user.save()

                try:
                    image_data = base64.b64decode(profile_image_data)
                    image = Image.open(BytesIO(image_data))
                    profile.profile_image.save("Img_" + name + ".png", ContentFile(image_data))
                    profile.save()
                except Exception as e:
                    print(f"Error decoding/processing image data: {e}")
                profile.gender = gender
                profile.save()

            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserProfileAPI(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile, context={'request': request})

        response_data = {
            "user_data": {
                "user_id": user_serializer.data["id"],
                "username": user_serializer.data["username"],
                "first_name": user_serializer.data["first_name"],
                "last_name": user_serializer.data["last_name"],
                "email": user_serializer.data["email"],
                "is_superuser": user_serializer.data["is_superuser"],
                "is_staff": user_serializer.data["is_staff"],
                "is_active": user_serializer.data["is_active"],
                "role": user_serializer.data["role"],
                "email": user_serializer.data["email"],
                "last_login": user_serializer.data["last_login"],
                "phone_number": profile_serializer.data["phone_number"],
                "age": profile_serializer.data["age"],
                "dob": profile_serializer.data["dob"],
                "gender": profile_serializer.data["gender"],
                "profile_image": request.build_absolute_uri(profile_serializer.data["profile_image"]),
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    user_id = request.data.get("user_id")
    user = CustomUser.objects.get(id=user_id)
    token, created = Token.objects.get_or_create(user=user)
    token.delete()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class RoleListView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    
class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all().order_by('mcc')
    serializer_class = LocationSerializer


class SubLocationListAPIView(generics.ListAPIView):
    serializer_class = SubLocationSerializer
    def get_queryset(self):
        location_id = self.kwargs['location_id']
        mcc = Location.objects.get(mcc_code = location_id)
        return SubLocations.objects.filter(mcc=mcc).order_by('mpp_loc')


@api_view(['POST'])
def create_farmer_feedback(request):
    if request.method == 'POST':
        serializer = FarmerFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackCategoryListAPIView(generics.ListAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer


class AddFarmerAPIView(APIView):
    def post(self, request, format=None):
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets

class VMCCsViewSet(viewsets.ModelViewSet):
    queryset = VMCCs.objects.all()
    serializer_class = VMCCsSerializer

class VMPPsViewSet(viewsets.ModelViewSet):
    queryset = VMPPs.objects.all()
    serializer_class = VMPPsSerializer


class FilterVMPPsViewSet(viewsets.ModelViewSet):
    queryset = VMPPs.objects.all()
    serializer_class = FilterVMPPsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mcc_code = self.request.query_params.get('mcc_code')
        print(f"Mcc Code: {mcc_code}")
        if mcc_code:
            queryset = queryset.filter(mcc_id=mcc_code)
        return queryset


from rest_framework import generics

class VCGroupListView(generics.ListAPIView):
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

from django.db.models import Q

class MonthAssignmentAPIView(APIView):
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
    queryset = ConductedByType.objects.all()
    serializer_class = ConductedByTypeSerializer

class ZeroDaysReasonViewSet(viewsets.ModelViewSet):
    queryset = ZeroDaysPourerReason.objects.all()
    serializer_class = ZeroDaysReasonSerializer

class MemberComplaintReasonViewSet(viewsets.ModelViewSet):
    queryset = MemberCompaintReason.objects.all()
    serializer_class = MemberComplaintReasonSerializer


class FacilitatorListView(viewsets.ModelViewSet):
    queryset = Facilitator.objects.all()
    serializer_class = FacilitatorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mcc_code = self.request.query_params.get('mcc_code')
        if mcc_code:
            queryset = queryset.filter(mcc_id=mcc_code)
        return queryset

class ConductedByNmeListView(viewsets.ModelViewSet):
    queryset = ConductedByName.objects.all()
    serializer_class = ConductedByNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.query_params.get('type_id')
        if type:
            queryset = queryset.filter(type_id=type_id)
        return queryset


class VMembersMobileViewSet(viewsets.ViewSet):
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

import base64
from django.core.files.base import ContentFile

class EndMeetingAPIView(APIView):
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


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class UserAuthentication(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({'message': 'Authentication successful'})
        else:
            return Response({'message': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

class ZeroDaysPouringReportList(APIView):
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
        

class CreateAwarenessAPIView(APIView):
    def post(self, request, *args, **kwargs):
        mpp_id = request.data.get('mpp_id')
        no_of_part = request.data.get('no_of_part')
        leader_name = request.data.get('leader_name')
        participants = request.data.get('participants',[])
        mpp = VMPPs.objects.get(mpp_loc_code=mpp_id)
        awareness = Awareness.objects.create(mpp=mpp,no_of_participants=no_of_part,leader_name=leader_name)
        for part in participants:
            participant = AwarenessTeamMembers.objects.create(awareness=awareness,member_name=part)
        response = {
            'message': 'Data Uploaded uccessfully',
            'meeting_id': awareness.id
        }
        return Response(response, status=status.HTTP_201_CREATED)
        
        
class AwarenessImagesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if 'images' in request.data:
            base64_images = request.data.get('images')
            id = request.data.get('id')
            awareness = Awareness.objects.get(id=id)
            print(id)
            for base64_image in base64_images:
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f"{random.randint(100, 999)}_{id}.jpg")
                meeting_image = AwarenessImages.objects.create(
                    awareness=awareness,
                    image=image_file,
                )
            response = {
                'message': 'Images uploaded successfully',
                'meeting_id': awareness.id
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No files were uploaded"}, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Count

class AwarenessListAPIView(generics.ListAPIView):
    serializer_class = AwarenessSerializer

    def get_queryset(self):
        queryset = Awareness.objects.annotate(num_images=Count('awareness_images'))
        return queryset.filter(num_images=0)


class VCGMeetingListAPIView(generics.ListAPIView):
    serializer_class = VCGMeetingSerializer

    def get_queryset(self):
        # queryset = VCGMeeting.objects.all()
        queryset = VCGMeeting.objects.annotate(num_images=Count('meeting_images'))
        # return queryset
        return queryset.filter(num_images=0)