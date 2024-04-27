from django.contrib import messages
from invent_app.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse
from  webpush import send_user_notification
from django.shortcuts import render, redirect, get_object_or_404
from invent_app.forms import FeedbackForm,MemberFeedbackForm,ForwardFeedbackForm,CloseFeedbackForm,ProfileUpdateForm
from invent_app.models import Feedback,LanguageSopported
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,TemplateView,UpdateView, DeleteView,DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from invent_app.utility.send_mail import *
from django.utils.translation import activate
from django.utils.translation import gettext as _
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.title import Title
from datetime import datetime
from openpyxl.chart.text import Text
from django.http import JsonResponse
from invent_app.utility.calculation import *
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from translate import Translator


languages = LanguageSopported.objects.all()

class CustomPermissionMixin(PermissionRequiredMixin):
    def has_permission(self):
        if super().has_permission():
            return True
        # Check individual user permissions
        if self.request.user.is_staff:
            return True
        
        user_permissions = self.request.user.get_all_permissions()
        try:
            
            if self.permission_required in user_permissions:
                return True

            user_groups = self.request.user.groups.all()
            for group in user_groups:
                if self.request.user.has_perm(self.permission_required, group=group):
                    return True
        except:
            pass
        return False
    
    def handle_no_permission(self):
        """
        Handles the case when the user doesn't have permission to access the view.
        """
        return HttpResponseForbidden(self.permission_denied_message)


class DashboardView(LoginRequiredMixin, CustomPermissionMixin, TemplateView):
    model = Feedback
    template_name = 'invent_app/myadmin/dashboard.html'
    context_object_name = 'feedbacks'
    success_url = 'dashboard'
    permission_required = ['invent_app.change_feedback', 'invent_app.view_feedback',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedbacks = Feedback.objects.all()
        context['feedbacks'] = feedbacks
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        member_feedback_list, member_feedback_count = self.get_member_feedback_data(False)
        member_closed_feedback_list, member_closed_feedback_count = self.get_member_feedback_data(True)
        context['m_feedback_list'] = member_feedback_list
        context['m_feedback_count'] = member_feedback_count
        sahayak_feedback_list, sahayak_feedback_count = self.get_sahayak_feedback_data(False)
        sahayak_closed_feedback_list, sahayak_closed_feedback_count = self.get_sahayak_feedback_data(True)
        context['s_feedback_list'] = sahayak_feedback_list
        context['s_feedback_count'] = sahayak_feedback_count
        context['closed_feedback'] = sahayak_closed_feedback_count+member_closed_feedback_count
        context['open_feedback'] = member_feedback_count+sahayak_feedback_count
        context['languages'] = languages
        context['role_codes'] = RoleCode
        return context
    
    def get_member_feedback_data(self,is_closed):
        if self.request.user.is_superuser or self.request.user.role.role_code == RoleCode.GRO.value:
            member_feedback_list = FarmerFeedback.objects.filter(is_closed=is_closed)
            
        elif self.request.user.role.role_code == RoleCode.HOD.value:
            member_feedback_list = FarmerFeedback.objects.filter(is_closed=is_closed,receiver_farmer=self.request.user)
        else:
            member_feedback_list = FarmerFeedback.objects.filter(sender=self.request.user,is_closed=is_closed)
        return member_feedback_list, member_feedback_list.count()

    def get_sahayak_feedback_data(self,is_closed):
        if self.request.user.is_superuser or self.request.user.role.role_code == RoleCode.GRO.value:
            sahyak_feedback_list = Feedback.objects.filter(is_closed=is_closed)
        elif self.request.user.role.role_code == RoleCode.HOD.value:
            sahyak_feedback_list = Feedback.objects.filter(is_closed=is_closed,receiver_feedback=self.request.user)
        else:
            sahyak_feedback_list = Feedback.objects.filter(sender=self.request.user,is_closed=is_closed)
        return sahyak_feedback_list, sahyak_feedback_list.count()
    
    def get_success_url(self):
        return self.success_url    


from itertools import chain

def get_notification(request):
    url = ''
    if request.user.is_superuser or request.user.role.role_code == RoleCode.GRO.value:
        member_feedback_list = FarmerFeedback.objects.filter(is_closed=False,receiver_farmer=None)

    else:
        member_feedback_list = FarmerFeedback.objects.filter(is_closed=False,receiver_farmer=request.user)
    if request.user.is_superuser or request.user.role.role_code == RoleCode.GRO.value:
        sahyak_feedback_list = Feedback.objects.filter(is_closed=False,receiver_feedback=None)
    else:
        sahyak_feedback_list = Feedback.objects.filter(is_closed=False,receiver_feedback=request.user)
    feedback_object = list(chain(member_feedback_list,sahyak_feedback_list))
    notification_list = []
    
    for obj in feedback_object:
        if isinstance(obj,Feedback):
            url = reverse('feedback_detail', kwargs={'pk': obj.id})
        elif isinstance(obj,FarmerFeedback):
            url = reverse('m_feedback_detail', kwargs={'pk': obj.id})
        
        notification_dict = {
            "title":f'{obj.sender.first_name} {obj.sender.last_name}' if obj.sender is not None else obj.name,
            'task':obj.feedback_cat.category,
            'time':obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'url':url
        }
        
        notification_list.append(notification_dict)
    return JsonResponse(notification_list,safe=False)


class SahayakFeedbackListView(LoginRequiredMixin, CustomPermissionMixin, ListView):
    model = Feedback
    template_name = 'invent_app/feedback_list.html'
    context_object_name = 'feedbacks'
    permission_required = ['invent_app.change_feedback', 'invent_app.view_feedback', 'invent_app.add_feedback']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(sender=self.request.user)
   
class MemberFeedbackListView(LoginRequiredMixin, CustomPermissionMixin, ListView):
    model = FarmerFeedback
    template_name = 'invent_app/m_feedback_list.html'
    context_object_name = 'feedbacks'
    permission_required = ['invent_app.change_feedback', 'invent_app.view_feedback', 'invent_app.add_feedback']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(sender=self.request.user)
   
class AllSahayakFeedbackListView(LoginRequiredMixin, CustomPermissionMixin, ListView):
    model = Feedback
    template_name = 'invent_app/feedback_list.html'
    context_object_name = 'feedbacks'
    permission_required = ['invent_app.change_feedback', 'invent_app.view_feedback', 'invent_app.add_feedback']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset.all()
        else:
            return queryset.filter(receiver_feedback=self.request.user)


class AllMemberFeedbackListView(LoginRequiredMixin, CustomPermissionMixin, ListView):
    model = FarmerFeedback
    template_name = 'invent_app/m_feedback_list.html'
    context_object_name = 'feedbacks'
    permission_required = ['invent_app.change_feedback', 'invent_app.view_feedback', 'invent_app.add_feedback']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset.all()
        else:
            return queryset.filter(receiver_farmer=self.request.user)

class FeedbackCreateView(LoginRequiredMixin, CustomPermissionMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'invent_app/feedback_form.html'
    success_url = reverse_lazy('final_submission')
    permission_required = 'invent_app.add_feedback'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        response = super().form_valid(form)
        try:            
            send_feedback_created_mail(request=self.request, feedback=self.object)
        except:
            messages.error(self.request, 'Error while sending email')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = get_object_or_404(Profile,user = self.request.user)
        try:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
        except:
            pass
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions      
        context['languages'] = languages  
        return context
    
    def get_success_url(self):
        return self.success_url

class MemberFeedbackCreateView(LoginRequiredMixin, CustomPermissionMixin, CreateView):
    model = FarmerFeedback
    form_class = MemberFeedbackForm
    template_name = 'invent_app/m_feedback_form.html'
    success_url = reverse_lazy('final_submission')
    permission_required = 'invent_app.add_feedback'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        response = super().form_valid(form)
        try:            
            send_member_feedback_created_mail(request=self.request, feedback=self.object)
        except:
            messages.error(self.request, 'Error while sending email')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context
    
    def get_success_url(self):
        return self.success_url


class FeedbackReviewView(TemplateView):
    template_name = 'invent_app/form_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_message = 'Your Feedback Has been Submitted Successfully'
        # Include data in the context
        context['submission_message'] = submission_message
        context['languages'] = languages
        # Pass the unsaved form instance to the template for preview
        context['feedback'] = self.request.session.get('unsaved_form_data')
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve unsaved form data from session
        unsaved_form_data = request.session.get('unsaved_form_data')
        if unsaved_form_data:
            # Create a form instance with the unsaved data
            form = FeedbackForm(unsaved_form_data)
            if form.is_valid():
                feedback_instance = form.save()
                del request.session['unsaved_form_data']
                return redirect('final_submission') 
            else:
                return render(request, 'invent_app/feedback_form.html', {'form': form})
        else:
            # Handle the case where there is no unsaved form data in the session
            # Redirect or render an appropriate response
            return redirect('some_other_view')  # Redirect to some other view


class FeedbackSubmitView(TemplateView):
    template_name = 'invent_app/final_submission.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_message = 'Your Feedback Has been Submitted Successfully'
        context['submission_message'] = submission_message
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('final_submission'))


class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'invent_app/detail_feedback.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

class MemberFeedbackDetailView(DetailView):
    model = FarmerFeedback
    template_name = 'invent_app/m_detail_feedback.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

class FeedbackDeleteView(LoginRequiredMixin, CustomPermissionMixin, DeleteView):
    model = Feedback
    template_name = 'invent_app/feedback_confirm_delete.html'
    success_url = reverse_lazy('feedback_list')
    permission_required = 'invent_app.delete_feedback'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

class MemberFeedbackDeleteView(LoginRequiredMixin, CustomPermissionMixin, DeleteView):
    model = FarmerFeedback
    template_name = 'invent_app/feedback_confirm_delete.html'
    success_url = reverse_lazy('m_feedback_list')
    permission_required = 'invent_app.delete_feedback'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

from django.views.generic import TemplateView,FormView
from django.shortcuts import get_object_or_404

class ForwardFeedbackView(FormView):
    template_name = 'invent_app/forward_feedback.html'
    success_url = 'feedback_list'
    
    form_class = ForwardFeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback_id = self.kwargs.get('pk')
        feedback = None
        if Feedback.objects.filter(feedback_id = feedback_id).exists():
           feedback = Feedback.objects.get(feedback_id = feedback_id)
        elif FarmerFeedback.objects.filter(feedback_id = feedback_id).exists():
            feedback = FarmerFeedback.objects.get(feedback_id = feedback_id)
        context['object'] = feedback
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        role = Role.objects.get(role_code='hod')
        kwargs['role'] = role
        return kwargs
    
    def form_valid(self, form):
        feedback_id = self.kwargs.get('pk')
        feedback = None
        if Feedback.objects.filter(feedback_id = feedback_id).exists():
           feedback = Feedback.objects.get(feedback_id = feedback_id)
           self.success_url = 'all_s_feedback_list'
        elif FarmerFeedback.objects.filter(feedback_id = feedback_id).exists():
            feedback = FarmerFeedback.objects.get(feedback_id = feedback_id)
            self.success_url = 'all_m_feedback_list'
        role = Role.objects.get(role_code='hod')
        user = form.cleaned_data['hods']
        feedback.forward_to_hod(role=role,department=user.department)
        feedback.save()
        messages.success(self.request, f'Feedback forwarded to {user}')
        send_feedback_forwarded_mail(request=self.request,feedback=feedback)
        return HttpResponseRedirect(reverse_lazy(self.success_url))


class CloseFeedbackView(FormView):
    template_name = 'invent_app/forward_feedback.html'
    success_url = 'feedback_list'
    form_class = CloseFeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback_id = self.kwargs.get('pk')
        feedback = None
        if Feedback.objects.filter(feedback_id = feedback_id).exists():
           feedback = Feedback.objects.get(feedback_id = feedback_id)
        elif FarmerFeedback.objects.filter(feedback_id = feedback_id).exists():
            feedback = FarmerFeedback.objects.get(feedback_id = feedback_id)
        context['object'] = feedback
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context
        
    def form_valid(self, form):
        feedback_id = self.kwargs.get('pk')
        feedback = None
        if Feedback.objects.filter(feedback_id = feedback_id).exists():
           feedback = Feedback.objects.get(feedback_id = feedback_id)
           self.success_url = 'all_s_feedback_list'
        elif FarmerFeedback.objects.filter(feedback_id = feedback_id).exists():
            feedback = FarmerFeedback.objects.get(feedback_id = feedback_id)
            self.success_url = 'all_m_feedback_list'
        remark = form.cleaned_data['remark']
        feedback.remark = remark
        feedback.close_feedback()
        feedback.save()
        send_feedback_status_mail(request=self.request,feedback=feedback)
        messages.success(self.request, f'Feedback {feedback.feedback_cat} is closed')
        return HttpResponseRedirect(reverse_lazy(self.success_url))


from django.http import JsonResponse
from invent_app.models import SubLocations, FeedbackCategory

def get_sublocations(request):
    location_id = request.GET.get('location_id')
    mcc = Location.objects.get(mcc_code=location_id)
    sublocations = SubLocations.objects.filter(mcc=mcc).order_by('mpp_loc')
    # Convert sublocations to a list of dictionaries
    data = [{'mpp_loc_code': sublocation.mpp_loc_code, 'mpp_loc': sublocation.mpp_loc} for sublocation in sublocations]
    return JsonResponse(data, safe=False)

def get_feedback_categories(request):
    feedback_categories = FeedbackCategory.objects.all().order_by('category')
    # data = {'<option value="{0}">{1}</option>'.format(category.id, category.category) for category in feedback_categories}
    data = [{'id': category.id, 'category': category.category} for category in feedback_categories]
    return JsonResponse(data, safe=False)

from django.utils import translation

def change_language(request):
    if request.method == 'POST':
        language_code = request.POST.get('language_code')
        translation.activate(language_code)
        response = JsonResponse({'success': True})
        response.set_cookie('django_language', language_code) # Set language preference in cookie
        request.session['django_language'] = language_code # Set language preference in session
        return response
    return JsonResponse({'success': False})

class ReportView(TemplateView):
    template_name = 'invent_app/report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_message = 'Your Feedback Has been Submitted Successfully'
        context['submission_message'] = submission_message
        user_permissions = self.request.user.get_all_permissions()
        context['user_permissions'] = user_permissions
        context['languages'] = languages
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('final_submission'))


def chart_data(request):
    series = []
    title = 'Feedbacks Yearly '
    yaxis = "No Of Feedbacks"
    hod_role = Role.objects.get(role_code = RoleCode.HOD.value)
    gro_role = Role.objects.get(role_code = RoleCode.GRO.value)
    sahayak_role = Role.objects.get(role_code = RoleCode.SAHAYAK.value)
    departments = None
    if request.user.role == hod_role:
        departments = Department.objects.filter(department = request.user.department)
    elif request.user.role == gro_role or request.user.is_superuser:
        departments = Department.objects.all()
    feedbacks_received = None
    year = datetime.now().year
    month = datetime.now().month
    feedback_counts = None
    if departments:
        for dept in departments:
            if CustomUser.objects.filter(department=dept, role=hod_role).exists():
                hod = CustomUser.objects.get(department=dept, role=hod_role)
                feedbacks_received = FarmerFeedback.objects.filter(receiver_farmer=hod)
                farmer_feedbacks = Feedback.objects.filter(receiver_feedback=hod)
                
                # Group feedbacks by month and count them
                feedback_counts = farmer_feedbacks.filter(created_at__year=datetime.now().year) \
                    .annotate(month=ExtractMonth('created_at')) \
                    .values('month') \
                    .annotate(total=Count('id'))

                member_feedback_counts = feedbacks_received.filter(created_at__year=datetime.now().year) \
                    .annotate(month=ExtractMonth('created_at')) \
                    .values('month') \
                    .annotate(total=Count('id'))
                data = [0] * 12  # Initialize data list with zeros for each month
                for feedback_count in feedback_counts:
                    month_index = feedback_count['month'] - 1  # Month index starts from 1
                    data[month_index] = feedback_count['total']
                for feedback_count in member_feedback_counts:
                    month_index = feedback_count['month'] - 1  # Month index starts from 1
                    data[month_index] = feedback_count['total']
                
                series.append({
                    "name": f'{hod.department.department} - {datetime.now().year}',
                    "data": data,
                    "dataLabels": {
                        "enabled": True
                    }
                })
    elif CustomUser.objects.filter(role=sahayak_role).exists():
        sayak = CustomUser.objects.get(id =request.user.id, role=sahayak_role)
        feedbacks = FarmerFeedback.objects.filter(sender=sayak)
        # Group feedbacks by month and count them
        feedback_counts = feedbacks.filter(created_at__year=datetime.now().year) \
            .annotate(month=ExtractMonth('created_at')) \
            .values('month') \
            .annotate(total=Count('id'))
        data = [0] * 12  # Initialize data list with zeros for each month
        for feedback_count in feedback_counts:
            month_index = feedback_count['month'] - 1  # Month index starts from 1
            data[month_index] = feedback_count['total']

        series.append({
            "name": f'{sayak.first_name} - {datetime.now().year}',
            "data": data,
            "dataLabels": {
                "enabled": True
            }
        })
    
    return JsonResponse(option_dictionary(series=series,title=title,xaxis=get_month_list(year=year),yaxis=yaxis,month='Months'))

def month_chart_data(request):
    series = []
    title = 'Feedbacks Monthly'
    yaxis = "No Of Feedbacks"
    hod_role = Role.objects.get(role_code = 'hod')
    gro_role = Role.objects.get(role_code = 'gro')
    sahayak_role = Role.objects.get(role_code = RoleCode.SAHAYAK.value)
    
    departments = None
    if request.user.role == hod_role:
        departments = Department.objects.filter(department = request.user.department)
    elif request.user.role == gro_role or request.user.is_superuser:
        departments = Department.objects.all()

    feedbacks_received = None
    year = datetime.now().year
    month = datetime.now().month
    if departments:
        for dept in departments:
            if CustomUser.objects.filter(department=dept, role=hod_role).exists():
                hod = CustomUser.objects.get(department=dept, role=hod_role)
                feedbacks_received = FarmerFeedback.objects.filter(receiver_farmer=hod)
                farmer_feedbacks = Feedback.objects.filter(receiver_feedback=hod)
                
                # Get the number of days in the current month
                num_days = calendar.monthrange(year, month)[1]
                
                data = [0] * num_days  # Initialize data list with zeros for each day
                
                # Get feedback counts for each day of the current month
                for day in range(1, num_days + 1):
                    feedback_count = farmer_feedbacks.filter(created_at__year=year,
                                                            created_at__month=month,
                                                            created_at__day=day).count()
                    member_feedback_count = feedbacks_received.filter(created_at__year=year,
                                                                    created_at__month=month,
                                                                    created_at__day=day).count()
                    # Sum up both feedback counts for the day
                    total_count = feedback_count + member_feedback_count
                    data[day - 1] = total_count  # Store the count for the day
                
                series.append({
                    "name": f'{hod.department.department} - {month}/{year}',
                    "data": data,
                    "dataLabels": {
                        "enabled": True
                    }
                })      
    elif CustomUser.objects.filter(role=sahayak_role).exists():
        sayak = CustomUser.objects.get(id =request.user.id, role=sahayak_role)
        feedbacks = FarmerFeedback.objects.filter(sender=sayak)
        # Group feedbacks by month and count them
        num_days = calendar.monthrange(year, month)[1]
        data = [0] * num_days  # Initialize data list with zeros for each day
        # Get feedback counts for each day of the current month
        for day in range(1, num_days + 1):
            feedback_count = feedbacks.filter(created_at__year=year,
                                                created_at__month=month,
                                                created_at__day=day).count()
            data[day - 1] = feedback_count  # Store the count for the day

        series.append({
            "name": f'{sayak.first_name} - {month}/{year}',
            "data": data,
            "dataLabels": {
                "enabled": True
            }
        })
                      
    return JsonResponse(option_dictionary(series=series,title=title,xaxis=get_current_month_dates(year,month),yaxis=yaxis,month=datetime.now().strftime('%B %Y')))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'invent_app/myadmin/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user.user_profile
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        return form
        
    def form_valid(self, form):
        profile = form.save(commit=False)
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        profile.save()
        return super().form_valid(form)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notification_test_page(request):
    current_user = request.user
    channel_layer = get_channel_layer()
    data = "notification" + "...." + str(datetime.now())
    user_id = str(current_user.pk)
    print(f'user-{user_id}')
    
    async_to_sync(channel_layer.group_send)(user_id,
        {
            "type": "notify",
            "text": data,
            'rejected_by': str(request.user)
        },
    )
    return render(request, 'invent_app/notify.html')



def notify(request):
    return render(request, 'index.html')


def notification(request):
    # Construct payload with URL
    notify_url = request.build_absolute_uri(reverse('user_profile'))
    notification_url = "https://kasheemilk.com"  # Replace this with the actual URL
    payload = {"head": "Low stock!", "body": "Stock is low. Please check ", "url": notification_url}
    
    # Send the notification
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    
    webpush = {"group": 'inventory' }
    return render(request, 'invent_app/notification.html', {"webpush": webpush})
