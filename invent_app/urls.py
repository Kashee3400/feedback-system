from django.urls import path
from .views.auth_views import LogoutView,LoginView
from .views import views,api_views
from .views.api_views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('login-user/', LoginView.as_view(), name='login_user'),
    path('logout-user/', LogoutView.as_view(), name='logout_user'),
    path('user-profile/', views.profile, name='user_profile'),
    path('product-list/', views.product_list, name='product_list'),
    path('notify/', views.notify, name='notify'),
    
    path('api/verify-email-otp/', EmailOTPVerificationView.as_view(), name='verify-email-otp'),
    path('api/send-email-otp/', SendOTPView.as_view(), name='send-otp'),

    path('api/update-profile/', update_profile_data, name='update_profile'),
    path('api/roles/', RoleListView.as_view(), name='role-list'),
    # logout API
    path('api/logout/', logout, name='logout'),

]
