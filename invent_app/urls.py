from django.urls import path
from .views.auth_views import LogoutView,LoginView,logout_then_login
from .views import views,api_views
from .views.api_views import *
from vcg.views import *
from awareness.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [

    path('', views.DashboardView.as_view(), name='dashboard'),
    # path('', views.notification, name='index'),
    path('set-language/', set_language, name='set_language'),
    path('login-user/', LoginView.as_view(), name='login_user'),
    path('api/authenticate/', UserAuthentication.as_view(), name='user-authentication'),
    
    path('logout-user/', logout_then_login, name='logout_user'),
    path('user-profile/', views.ProfileUpdateView.as_view(), name='user_profile'),
    path('notify/', views.notify, name='notify'),
    
    path('create-feedback/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('m-create-feedback/', views.MemberFeedbackCreateView.as_view(), name='m_feedback_create'),
    path('review-form/', views.FeedbackReviewView.as_view(), name='review_form'),
    path('final_submission/', views.FeedbackSubmitView.as_view(), name='final_submission'),
    path('sahayak-feedbacks/', views.SahayakFeedbackListView.as_view(), name='feedback_list'),
    path('member-feedbacks/', views.MemberFeedbackListView.as_view(), name='m_feedback_list'),
    path('all-sahayak-feedbacks/', views.AllSahayakFeedbackListView.as_view(), name='all_s_feedback_list'),
    path('all-member-feedbacks/', views.AllMemberFeedbackListView.as_view(), name='all_m_feedback_list'),
    path('hod-feedbacks/', views.SahayakFeedbackListView.as_view(), name='hod_feedback_list'),
    # path('update-feedback/<int:pk>/', views.FeedbackUpdateView.as_view(), name='feedback_update'),
    path('delete-feedback/<int:pk>/', views.FeedbackDeleteView.as_view(), name='feedback_delete'),
    path('m-delete-feedback/<int:pk>/', views.MemberFeedbackDeleteView.as_view(), name='m_feedback_delete'),
    path('feedback-details/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('m-feedback-details/<int:pk>/', views.MemberFeedbackDetailView.as_view(), name='m_feedback_detail'),
    path('get_sublocations/', views.get_sublocations, name='get_sublocations'),
    path('get_feedback_categories/', views.get_feedback_categories, name='get_feedback_categories'),
    path('forward-feedback/<str:pk>/', views.ForwardFeedbackView.as_view(), name='forward_feedback'),
    path('close-feedback/<str:pk>/', views.CloseFeedbackView.as_view(), name='close_feedback'),
    path('get-notification/', views.get_notification, name='get_notification'),
    path('change-language/', views.change_language, name='change_language'),
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('chart-data/', views.chart_data, name='chart_data'),
    path('month-chart-data/', views.month_chart_data, name='month_chart_data'),
    
    path('api/verify-email-otp/', EmailOTPVerificationView.as_view(), name='verify-email-otp'),
    path('api/send-email-otp/', SendOTPView.as_view(), name='send-otp'),

    path('api/update-profile/', update_profile_data, name='update_profile'),
    path('api/roles/', RoleListView.as_view(), name='role-list'),
    
    # Veterinary Module URLS
    path('vet-dashboard', views.VetDashboardView.as_view(),name='vet_dashboard'),
    
    # VCG Urs
    path('api/logout/', logout, name='logout'),
    path('api/locations/', LocationListAPIView.as_view(), name='location-list'),
    path('api/locations/<str:location_id>/sublocations/', SubLocationListAPIView.as_view(), name='sublocation-list'),
    path('api/feedback-categories/', FeedbackCategoryListAPIView.as_view(), name='feedback-category-list'),
    path('api/vmpps/<str:mcc_code>/', VMPPsViewSet.as_view({'get': 'list'}), name='vmpps-list'),
    path('api/vcg-group/', VCGroupListView.as_view(), name='vcg-group-list'),
    path('api/mark-attendance/', MarkVCGMemberAttendance.as_view(), name='mark_attendance'),
    path('api/start-meeting/', StartMeetingAPIView.as_view(), name='start_meeting'),
    path('api/zero-days-report/', ZeroDaysReasonReport.as_view(), name='zero_days_report'),
    path('api/complaint-report/', ComplaintReport.as_view(), name='complaint_report'),
    path('api/end-meeting/', EndMeetingAPIView.as_view(), name='end_meeting'),
    path('api/month-assignment/', MonthAssignmentAPIView.as_view(), name='month_assignment'),
    path('api/zerodays-pouring/', ZeroDaysPouringReportList.as_view(), name='zerodays-pouring-list'),
    path('api/member-complaints/', MemberComplaintReportList.as_view(), name='member-complaints-list'),
    path('api/vcg-meeting-list/', VCGMeetingListAPIView.as_view(), name='vcg_meeting_list'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Awareness Program APIs
    path('api/create-awareness/', CreateAwarenessAPIView.as_view(), name='create_awareness'),
    path('api/upload-awareness-images/', AwarenessImagesAPIView.as_view(), name='upload-awareness-images'),
    path('api/awareness/', AwarenessListAPIView.as_view(), name='awareness-list'),


    path('feedback/create/emp/', views.EmpFeedbackCreateView.as_view(), name='feedback_emp_create'),
    path('feedback/<int:pk>/change-status/', views.FeedbackChangeStatusView.as_view(), name='feedback_emp_change_status'),
    path('feedback/<int:pk>/forward/emp/', views.FeedbackForwardView.as_view(), name='feedback_emp_detail'),
    path('feedback/list/emp/', views.AllEMPFeedbackListView.as_view(), name='feedback_emp_list'),
    path('search-feedback-logs/', views.search_feedback_logs, name='search_feedback_logs'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
