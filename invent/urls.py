from django.contrib import admin
from django.urls import path,include,re_path
from invent_app.views import views,api_views
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vmccs', api_views.VMCCsViewSet, basename='vmccs')
router.register(r'vmpps', api_views.FilterVMPPsViewSet, basename='vmpps')
router.register(r'facilitators', api_views.FacilitatorListView, basename='facilitators')
router.register(r'conductedbyname', api_views.ConductedByNmeListView, basename='conductedbyname')
router.register(r'members', api_views.VMembersMobileViewSet, basename='members_list')
router.register(r'conducted-types', api_views.ConductedByTypeViewSet, basename='conducted-types')
router.register(r'zero-days-reason', api_views.ZeroDaysReasonViewSet, basename='zerodays-reason')
router.register(r'complaint-reason', api_views.MemberComplaintReasonViewSet, basename='complaint-reason')

admin.site.site_title = "Nachiketa Admin"

    # Text to put in each page's <div id="site-name">.
admin.site.site_header = "Nachiketa Administration"

    # Text to put at the top of the admin index page.
admin.site.index_title = "Nachiketa administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invent_app.urls')),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^webpush/', include('webpush.urls')),
    path('notification/', views.notification, name="notification"),
    path('mynotify/', views.notification_test_page, name="notify"),
]
