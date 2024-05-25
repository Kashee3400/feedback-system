from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
import base64
from .serializers import *
from django.core.files.base import ContentFile


class CreateAwarenessAPIView(APIView):
    def post(self, request, *args, **kwargs):
        mpp_id = request.data.get('mpp_id')
        no_of_part = request.data.get('no_of_part')
        leader_name = request.data.get('leader_name')
        participants = request.data.get('participants', [])
        
        if not all([mpp_id, no_of_part, leader_name]):
            return Response({'message': 'MPP ID, number of participants, and leader name are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not participants:
            return Response({'message': 'At least one participant is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        awareness = Awareness.objects.create(mpp_id=mpp_id, no_of_participants=no_of_part, leader_name=leader_name)
        print(awareness);
        for part in participants:
            participant = AwarenessTeamMembers.objects.create(awareness=awareness, member_name=part)

        response = {
            'message': 'Data Uploaded successfully',
            'meeting_id': awareness.id
        }
        return Response(response, status=status.HTTP_201_CREATED)


class AwarenessImagesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if 'images' in request.data:
            base64_images = request.data.get('images')
            id = request.data.get('id')
            awareness = Awareness.objects.get(id=id)
            for base64_image in base64_images:
                image_data = base64.b64decode(base64_image)
                image_file = ContentFile(image_data, name=f"{random.randint(100, 999)}_{id}.jpg")
                meeting_image = AwarenessImages.objects.create(
                    awareness=awareness,
                    image=image_file,
                )
            response = {
                'message': 'Images uploaded successfully',
                'meeting_id': awareness.id
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No files were uploaded"}, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Count

class AwarenessListAPIView(generics.ListAPIView):
    serializer_class = AwarenessSerializer

    def get_queryset(self):
        queryset = Awareness.objects.annotate(num_images=Count('awareness_images'))
        return queryset.filter(num_images=0)
