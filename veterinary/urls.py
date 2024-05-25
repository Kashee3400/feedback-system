from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = DefaultRouter()
router.register(r'tagtypes', TAGTypeViewSet)
router.register(r'cattle-case-types', CattleCaseTypeViewSet)
router.register(r'time-slots', TimeSlotViewSet)
router.register(r'diagnosis-routes', DiagnosisRouteViewSet)
router.register(r'symptoms', SymptomsViewSet)
router.register(r'diseases', DiseaseViewSet)
router.register(r'cattle-tagging', CattleTaggingViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'caseentries', CaseEntryViewSet)

urlpatterns = [
    path('api/add_farmer/', AddFarmerAPIView.as_view(), name='add_farmer'),
    path('api/', include(router.urls)),
    
    #************************JWT Token ******************************#
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/farmer-cattles/', CattleListView.as_view(), name='cattle-list'),
]