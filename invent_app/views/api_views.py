from rest_framework import generics, status
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.decorators import api_view
import base64
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from invent_app.serializers import *
import random
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.utils import timezone
from invent_app.models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



def generate_otp():
    digits = "0123456789"
    return ''.join(random.choice(digits) for _ in range(6))


def create_otp(user):
    expiry_time = timezone.now() + timedelta(minutes=1)    
    # Generate the OTP token
    otp_token = generate_otp()
    # Create the OTPToken object with user, token, and expiry time
    otp_token_obj = OTPToken.objects.create(user=user, token=otp_token, expiry_time=expiry_time)
    
    return otp_token_obj

class SendOTPView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            user = ""
            if email:
                if CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.get(email=email)
                else:    
                    return JsonResponse({'message': f'User {email} not exists. Please contact admin'}, status=400)
                otp = create_otp(user)
                subject = 'Feedbacks System OTP verification'
                to_email = [email]
                logo = Logo.objects.all()
                html_content = render_to_string(
                    'api/otp_email_template.html', {'otp': otp, 'for': 'login', 'logo': logo})
                email = EmailMessage(subject, html_content,
                                     settings.EMAIL_HOST_USER, to_email)
                email.content_subtype = 'html'
                email.send()
                return JsonResponse({'message': "OTP sent successfully!!"})
            else:
                return JsonResponse({'message': 'Email is required'}, status=400)
        else:
            return JsonResponse({'response': 'error while sending the OTP'})


class EmailOTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_token = request.data.get('otp')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            if verify_otp(user, otp_token):
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                data ={'message': 'Logged in successfully', 
                       'status':200,
                       'token': token.key,
                       "user_id":user.id
                       }
                return Response(data, status=status.HTTP_200_OK)
            else:
                OTPToken.objects.all().delete()
                return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except OTPToken.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def verify_otp(user, otp):
    otp_token = OTPToken.objects.filter(
        user=user, token=otp).order_by('-created_at').last()
    if otp_token:
        time_difference = timezone.now() - otp_token.created_at
        # OTP expires after 5 minutes (300 seconds)
        if time_difference.seconds < 300:
            otp_token.delete()
            return True
    return False

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_data(request):
    try:
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get("user_id")
            profile = Profile.objects.get(user=user_id)
            if profile.profile_image:
                existing_image_path = profile.profile_image.path
                default_storage.delete(existing_image_path)
            if 'phone_number' in serializer.validated_data:
                profile.phone_number = serializer.validated_data['phone_number']
            if 'profile_image' in serializer.validated_data:
                profile_image_data = serializer.validated_data['profile_image']
                gender = serializer.validated_data['gender']
                email = serializer.validated_data['email']
                name = serializer.validated_data['name']
                try:
                    user = CustomUser.objects.get(email=email)
                    if user.id != user_id:
                        return Response({"message": "Email is already associated with another user."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user.first_name = name
                        user.save()

                except CustomUser.DoesNotExist:
                    user = CustomUser.objects.get(pk=user_id)
                    user.username = email
                    user.email = email
                    user.first_name = name
                    user.save()

                try:
                    image_data = base64.b64decode(profile_image_data)
                    image = Image.open(BytesIO(image_data))
                    profile.profile_image.save("Img_" + name + ".png", ContentFile(image_data))
                    profile.save()
                except Exception as e:
                    print(f"Error decoding/processing image data: {e}")
                profile.gender = gender
                profile.save()

            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserProfileAPI(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile, context={'request': request})

        response_data = {
            "user_data": {
                "user_id": user_serializer.data["id"],
                "username": user_serializer.data["username"],
                "first_name": user_serializer.data["first_name"],
                "last_name": user_serializer.data["last_name"],
                "email": user_serializer.data["email"],
                "is_superuser": user_serializer.data["is_superuser"],
                "is_staff": user_serializer.data["is_staff"],
                "is_active": user_serializer.data["is_active"],
                "role": user_serializer.data["role"],
                "email": user_serializer.data["email"],
                "last_login": user_serializer.data["last_login"],
                "phone_number": profile_serializer.data["phone_number"],
                "age": profile_serializer.data["age"],
                "dob": profile_serializer.data["dob"],
                "gender": profile_serializer.data["gender"],
                "profile_image": request.build_absolute_uri(profile_serializer.data["profile_image"]),
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    user_id = request.data.get("user_id")
    user = CustomUser.objects.get(id=user_id)
    token, created = Token.objects.get_or_create(user=user)
    token.delete()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

from rest_framework.permissions import AllowAny

class RoleListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    
class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all().order_by('mcc')
    serializer_class = LocationSerializer


class SubLocationListAPIView(generics.ListAPIView):
    serializer_class = SubLocationSerializer
    def get_queryset(self):
        location_id = self.kwargs['location_id']
        mcc = Location.objects.get(mcc_code = location_id)
        return SubLocations.objects.filter(mcc=mcc).order_by('mpp_loc')


@api_view(['POST'])
def create_farmer_feedback(request):
    if request.method == 'POST':
        serializer = FarmerFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackCategoryListAPIView(generics.ListAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer
