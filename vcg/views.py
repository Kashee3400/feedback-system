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
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext_lazy as _
from datetime import timedelta,datetime
from django.template.loader import render_to_string
from django.conf import settings
from django.views import View
from urllib.parse import urlparse
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import make_aware,make_naive
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from django.db import IntegrityError, transaction
import logging
from django.core.files.storage import FileSystemStorage


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
                'status':status_code,
                'message': 'Successful',
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
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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


from django.core.exceptions import ObjectDoesNotExist

class StartMeetingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        try:
            data = request.data
            mpp_id = data.get('mpp_id')
            type = data.get('type')
            type_id = data.get('type_id')
            conducted_by_name_id = data.get('conducted_by_name_id')
            date_time = data.get('date_time')

            # Validate required fields
            if not all([mpp_id, type, type_id, conducted_by_name_id, date_time]):
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')

            # Get required objects
            mpp = VMPPs.objects.get(mpp_loc_code=mpp_id)
            c_type = ConductedByType.objects.get(id=type_id)
            facilitator = None
            conducted_by_name = None
            if type == 'Facilitator':
                    facilitator = Facilitator.objects.get(id=conducted_by_name_id)
            else:
                    conducted_by_name = ConductedByName.objects.get(id=conducted_by_name_id)                    
            # Create a new meeting
            meeting = VCGMeeting.objects.create(
                user=self.request.user,
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
            return Response(response, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': f'Invalid date format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConductedByTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = ConductedByType.objects.all()
    serializer_class = ConductedByTypeSerializer

class ZeroDaysReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = ZeroDaysPourerReason.objects.all()
    serializer_class = ZeroDaysReasonSerializer

class MemberComplaintReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = MemberCompaintReason.objects.all()
    serializer_class = MemberComplaintReasonSerializer


class FacilitatorListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Facilitator.objects.all()
    serializer_class = FacilitatorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mcc_code = self.request.query_params.get('mcc_code')
        if mcc_code:
            queryset = queryset.filter(mcc_id=mcc_code)
        return queryset

class ConductedByNmeListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = ConductedByName.objects.all()
    serializer_class = ConductedByNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.query_params.get('type_id')
        if type:
            queryset = queryset.filter(type_id=type_id)
        return queryset


class VMembersMobileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
            return Response(response, status=status.HTTP_200_OK)
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = VCGMeetingSerializer


    def get_queryset(self):
        user = self.request.user
        queryset = VCGMeeting.objects.annotate(num_images=Count('meeting_images'))
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(user=user,num_images=0)
    
from django.views.generic import ListView
from .models import VCGMeeting
from django.db.models import Q

class VCGMeetingDetailedReport(ListView):
    model = VCGMeeting
    template_name = 'vcg/report.html'
    context_object_name = 'vcg_meetings'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
       
        return queryset
    
    def post(self, request, *args, **kwargs):
        # Custom logic for POST request
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def put(self, request, *args, **kwargs):
        # Custom logic for PUT request
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        # Custom logic for DELETE request
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vmpps_without_vcg_meetings = VMPPs.objects.filter(mpp_vcg_meetings__isnull=True)
        context['vmpps_without_vcg_meetings'] = vmpps_without_vcg_meetings
        context['status_choices'] = VCGMeeting.STATUS_CHOICES
        context['status_filter'] = self.request.GET.get('status', '')
        return context
    
    
    def render_to_response(self, context, **response_kwargs):
        # Custom logic for rendering the response
        response = super().render_to_response(context, **response_kwargs)
        response['Custom-Header'] = 'CustomValue'
        return response

from django.views.generic import DetailView
from django.http import Http404, HttpResponse

class VCGMeetingDetailView(DetailView):
    model = VCGMeeting
    template_name = 'vcg/vcgmeeting_detail.html'
    context_object_name = 'vcg_meeting'

    def get(self, request, *args, **kwargs):
        # Custom logic for GET request
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Custom logic for POST request
        return HttpResponse('POST request is not allowed for this view', status=405)

    def put(self, request, *args, **kwargs):
        # Custom logic for PUT request
        return HttpResponse('PUT request is not allowed for this view', status=405)

    def delete(self, request, *args, **kwargs):
        # Custom logic for DELETE request
        return HttpResponse('DELETE request is not allowed for this view', status=405)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here
        context['extra_info'] = 'Additional context if needed'
        return context

    def get_object(self, queryset=None):
        # Custom logic to get the object
        return super().get_object(queryset)

    def get_queryset(self):
        # Custom logic to get the queryset
        return super().get_queryset()

    def get_template_names(self):
        # Custom logic to get the template names
        return [self.template_name]

    def render_to_response(self, context, **response_kwargs):
        # Custom logic for rendering the response
        response = super().render_to_response(context, **response_kwargs)
        response['Custom-Header'] = 'CustomValue'
        return response

    def handle_no_permission(self):
        # Custom logic for handling no permission
        return HttpResponse('You do not have permission to view this page', status=403)


from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from .forms import (
    MppVisitByForm, CompositeDataForm, DispatchDataForm,
    MaintenanceChecklistForm, NonPourerMeetForm, VcgMeetingForm, MembershipAppForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import transaction, IntegrityError
from formtools.wizard.views import SessionWizardView
from .models import EventSession, FormProgress
from .forms import MppVisitByForm, CompositeDataForm, DispatchDataForm, MaintenanceChecklistForm, NonPourerMeetForm, VcgMeetingForm, MembershipAppForm

FORMS = [
    ('facilitator', MppVisitByForm),
    ('composite_data', CompositeDataForm),
    ('dispatch_data', DispatchDataForm),
    ('maintenance_checklist', MaintenanceChecklistForm),
    ('non_pourer_meet', NonPourerMeetForm),
    ('vcg_meeting', VcgMeetingForm),
    ('membership_app', MembershipAppForm),
]

TEMPLATES = {
    'facilitator': 'mppvisit/facilitator.html',
    'composite_data': 'mppvisit/composite_data.html',
    'dispatch_data': 'mppvisit/dispatch_data.html',
    'maintenance_checklist': 'mppvisit/maintenance_checklist.html',
    'non_pourer_meet': 'mppvisit/non_pourer_meet.html',
    'vcg_meeting': 'mppvisit/vcg_meeting.html',
    'membership_app': 'mppvisit/membership_app.html',
}

from django.contrib import messages

class DataCollectionWizard(SessionWizardView):
    template_name = 'mppvisit/visit-form.html'
    url_name = reverse_lazy('home')  # Replace with the correct URL name

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_user_instance(self):
        """
        Get or create the EventSession instance based on the session name from the URL.
        If no session exists, create a new one when the form is first rendered.
        """
        session_name = self.kwargs.get('session_name')

        # Check if the session is already created and stored in the wizard's storage
        session_id = self.storage.data.get('session_id')
        if session_id:
            return get_object_or_404(EventSession, id=session_id)

        # If session_name exists, try to fetch the session
        if session_name:
            try:
                session = EventSession.objects.get(session_name=session_name)
                self.storage.data['session_id'] = session.id
                return session
            except EventSession.DoesNotExist:
                pass  # Handle the case where session_name does not exist

        # If no session_name or no existing session, create a new one
        new_session = EventSession.objects.create()
        self.storage.data['session_id'] = new_session.id
        return new_session

    def get_form_initial(self, step):
        """
        Load the saved form data for the user if it exists. If no user, return an empty form.
        """
        session = self.get_user_instance()
        if session:
            progress = FormProgress.objects.filter(session=session, step=step).first()
            if progress:
                return progress.data
        return super().get_form_initial(step)

    def get_form(self, step=None, **kwargs):
        form = super().get_form(step, **kwargs)
        if step == 'non_pourer_meet':
            mpp_form_data = self.get_form_initial('facilitator')
            mpp = mpp_form_data.get('mpp') if mpp_form_data else None
            form = NonPourerMeetForm(**kwargs, mpp=mpp) 
        return form
    

    def post(self, *args, **kwargs):
        current_step = self.steps.current
        session = self.get_user_instance()
        form = self.get_form(current_step, data=self.request.POST)
        print(self.request.POST)
        if form.is_valid():
            if current_step == 'non_pourer_meet':
                if self.request.POST.get('want_to_add_more'):
                    try:
                        form.save(commit=False)
                        meet = form.instance
                        meet.session_id = session.pk
                        meet.save()
                        messages.success(self.request, 'Record added successfully. You can add more records now.')
                        return self.render(self.get_form(current_step))
                    except Exception as e:
                        messages.error(self.request, f'An error occurred while saving the record: {str(e)}')
                        return self.render(form)
                else:
                    messages.success(self.request, 'Record saved successfully. Moving to the next step.')
                    return super().post(*args, **kwargs)
            else:
                try:
                    self.save_form_data(session, current_step, form.cleaned_data)
                    messages.success(self.request, f'Successfully completed step: {current_step}.')
                    return super().post(*args, **kwargs)
                except Exception as e:
                    messages.error(self.request, f'An error occurred while processing the step: {str(e)}')
                    return self.render(form)
        else:
            messages.error(self.request, 'Please correct the errors below.')
            return self.render(form)

    def save_form_data(self, session, current_step, form_data):
        """
        Save form data securely and handle rollback in case of failure.
        """
        try:
            FormProgress.objects.update_or_create(
                session=session, step=current_step, defaults={'data': form_data}
            )
        except IntegrityError as e:
            messages.error(self.request, "An error occurred while saving your data. Please try again.")
            raise

    def done(self, form_list, **kwargs):
        try:
            with transaction.atomic():
                mppvisitby_form = form_list[0]
                composite_data_form = form_list[1]
                dispatch_data_form = form_list[2]
                maintenance_checklist_form = form_list[3]
                non_pourer_form = form_list[4]
                vcg_meeting_form = form_list[5]
                membership_app_form = form_list[6]

                session = self.get_user_instance()

                mppvisitby = mppvisitby_form.save(commit=False)
                mppvisitby.session = session
                mppvisitby.save()

                composite_data = composite_data_form.save(commit=False)
                composite_data.session = session
                composite_data.save()

                dispatch_data = dispatch_data_form.save(commit=False)
                dispatch_data.session = session
                dispatch_data.save()

                maintenance_checklist_data = maintenance_checklist_form.save(commit=False)
                maintenance_checklist_data.session = session
                maintenance_checklist_data.save()

                non_pourer_data = non_pourer_form.save(commit=False)
                non_pourer_data.session = session
                non_pourer_data.save()


                vcg_meeting_data = vcg_meeting_form.save(commit=False)
                vcg_meeting_data.session = session
                vcg_meeting_data.save()

                membership_app_data = membership_app_form.save(commit=False)
                membership_app_data.session = session
                membership_app_data.save()

                FormProgress.objects.filter(session=session).update(status='completed')

                return redirect('create_mppvisit')
            
        except IntegrityError as e:
            messages.error(self.request, "An error occurred while finalizing your data. Please try again.")
            return self.render_error_page()

    def render_error_page(self):
        return redirect('error_page')
