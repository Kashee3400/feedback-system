from django.shortcuts import render
from rest_framework import generics, status
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.decorators import api_view
import base64
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from invent_app.serializers import *
from django.shortcuts import render, get_object_or_404
import random
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.contrib import messages
from django.utils import timezone
from invent_app.models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import FarmerSerializer
# Create your views here.


class AddFarmerAPIView(APIView):
    def post(self, request, format=None):
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
