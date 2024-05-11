from rest_framework import generics, status
from django.core.files.base import ContentFile
from PIL import Image
import base64
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from invent_app.serializers import *
import random
from django.core.files.storage import default_storage
from rest_framework.response import Response
from invent_app.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import viewsets
from .models import *


class AddFarmerAPIView(APIView):
    def post(self, request, format=None):
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TAGTypeViewSet(viewsets.ModelViewSet):
    queryset = TAGType.objects.all()
    serializer_class = TAGTypeSerializer


class CattleCaseTypeViewSet(viewsets.ModelViewSet):
    queryset = CattleCaseType.objects.all()
    serializer_class = CattleCaseTypeSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    
class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class DiagnosisRouteViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisRoute.objects.all()
    serializer_class = DiagnosisRouteSerializer

class SymptomsViewSet(viewsets.ModelViewSet):
    queryset = Symptoms.objects.all()
    serializer_class = SymptomsSerializer

class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class CattleTaggingViewSet(viewsets.ModelViewSet):
    queryset = CattleTagging.objects.all()
    serializer_class = CattleTaggingSerializer