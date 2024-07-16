from vcg import views
from django.urls import path


urlpatterns = [
    path('dashboard/', views.VCGMeetingDetailedReport.as_view(), name='vcg_dashboard' ),
    path('vcgmeeting/<int:pk>/', views.VCGMeetingDetailView.as_view(), name='vcgmeeting_detail'),
]
