from django.contrib import admin
from django.urls import path,include,re_path
from invent_app.views.api_views import FarmerFeedbackViewSet
from invent_app.views import views
from vcg import views
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vmccs', views.VMCCsViewSet, basename='vmccs')
router.register(r'vmpps', views.FilterVMPPsViewSet, basename='vmpps')
router.register(r'facilitators', views.FacilitatorListView, basename='facilitators')
router.register(r'conductedbyname', views.ConductedByNmeListView, basename='conductedbyname')
router.register(r'members', views.VMembersMobileViewSet, basename='members_list')
router.register(r'conducted-types', views.ConductedByTypeViewSet, basename='conducted-types')
router.register(r'zero-days-reason', views.ZeroDaysReasonViewSet, basename='zerodays-reason')
router.register(r'complaint-reason', views.MemberComplaintReasonViewSet, basename='complaint-reason')
router.register(r'farmer-feedback', FarmerFeedbackViewSet, basename="farmer_feedback")

admin.site.site_title = "Nachiketa Admin"

    # Text to put in each page's <div id="site-name">.
admin.site.site_header = "Nachiketa Administration"

    # Text to put at the top of the admin index page.
admin.site.index_title = "Nachiketa administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invent_app.urls')),
    path('vet/', include('veterinary.urls')),
    path('vcg/', include('vcg.urls')),
    path('route/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create-mppvisit/', views.DataCollectionWizard.as_view(views.FORMS), name='create_mppvisit'),
    path('event-sessions/', views.EventSessionListView.as_view(), name='event_session_list'),
    re_path(r'^webpush/', include('webpush.urls')),
]
