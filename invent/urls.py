from django.contrib import admin
from django.urls import path,include,re_path
from invent_app.views import views

admin.site.site_title = "Feedback Admin"

    # Text to put in each page's <div id="site-name">.
admin.site.site_header = "Feedback Administration"

    # Text to put at the top of the admin index page.
admin.site.index_title = "Site administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invent_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^webpush/', include('webpush.urls')),
    path('notification/', views.notification, name="notification"),
    path('mynotify/', views.notification_test_page, name="notify"),

]
