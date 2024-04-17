from django.urls import path
from .views.auth_views import LogoutView,LoginView,logout_then_login
from .views import views,api_views
from .views.api_views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    # path('', views.notification, name='index'),
    path('set-language/', set_language, name='set_language'),
    path('login-user/', LoginView.as_view(), name='login_user'),
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
    # logout API
    path('api/logout/', logout, name='logout'),
    path('api/locations/', LocationListAPIView.as_view(), name='location-list'),
    path('api/locations/<str:location_id>/sublocations/', SubLocationListAPIView.as_view(), name='sublocation-list'),
    path('api/feedback-categories/', FeedbackCategoryListAPIView.as_view(), name='feedback-category-list'),
    path('api/feedback-create/', create_farmer_feedback, name='create_feedback'),
    path('api/add_farmer/', AddFarmerAPIView.as_view(), name='add_farmer'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
