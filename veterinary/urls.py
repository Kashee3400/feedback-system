from django.urls import path
from .views import *

urlpatterns = [
    path('api/add_farmer/', AddFarmerAPIView.as_view(), name='add_farmer'),
]