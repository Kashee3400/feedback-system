from vcg import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('dashboard/', views.VCGMeetingDetailedReport.as_view(), name='vcg_dashboard' ),
    path('vcgmeeting/<int:pk>/', views.VCGMeetingDetailView.as_view(), name='vcgmeeting_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('session-details/<str:name>/', views.MppVisirReportView.as_view(), name='session_details'),
    
]
