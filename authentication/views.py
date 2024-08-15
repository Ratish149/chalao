from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,GenericAPIView,RetrieveUpdateAPIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer,LoginSerializer,UserProfileSerializer,VendorProfileSerializer
from django.contrib.auth import authenticate
from .models import User,UserProfile,VendorProfile

# Create your views here.

class UserSignupView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        otp = get_random_string(length=6,allowed_chars='0123456789')
        user.otp = otp
        user.save()
        
        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            'bdevil149@gmail.com',
            ['ratish.shakya149@gmail.com'],
            fail_silently=False,
        )
        refresh = RefreshToken.for_user(user)
        
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response(
                    {
                    'refresh': refresh_token,
                    'access': access_token,
                })

class VerifyOTPView(GenericAPIView):
   
    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user=request.user
        try:
            if user.otp == otp:
                user.is_verified = True
                user.otp=""
                user.save()
                return Response({'detail': 'Email verified successfully'})
            else:
                return Response({'detail': 'Invalid OTP'})
        except User.DoesNotExist:
            return Response({'detail': 'Invalid OTP'})
               

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username=request.data.get('username')
        password=request.data.get('password')

        user=authenticate(username=username,password=password)

        if user is not None:
            if user.is_verfied:
                return Response({'Message':'Login Successful!'})
            else:
                return Response({'Message':'OTP Failed'})
        else:
            return Response({'Message':'Login Failed'})
        
class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = VendorProfileSerializer(user_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        data=request.data

        user_profile.license_number = data.get('license_number')
        user_profile.expiry_date = data.get('expiry_date')
        user_profile.issued_district = data.get('issued_district')
        user_profile.driving_license_front = data.get('driving_license_front')
        user_profile.driving_license_back = data.get('driving_license_back')

        user_data=data.get('user')
        user = user_profile.user
        user.full_name = user_data.get('full_name')
        user.phonenumber = user_data.get('phonenumber')
        user.address = user_data.get('address')
        user.dateofbirth = user_data.get('dateofbirth')
        user.gender = user_data.get('gender')
        user.occupation = user_data.get('occupation')
        user.citizenship_number = user_data.get('citizenship_number')
        user.nid_number = user_data.get('nid_number')
        user.issued_date = user_data.get('issued_date')
        user.issued_district = user_data.get('issued_district')
        user.citizenship_front = user_data.get('citizenship_front')
        user.citizenship_back = user_data.get('citizenship_back')

        user_profile.save()
        user.save()
        return Response({'detail': 'Profile updated successfully','Data':UserProfileSerializer(user_profile).data})

class VendorProfileView(RetrieveUpdateAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

    def get(self, request, *args, **kwargs):
        vendor_profile = VendorProfile.objects.get(user=request.user)
        serializer = VendorProfileSerializer(vendor_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        vendor_profile = VendorProfile.objects.get(user=self.request.user)
        data=request.data

        vendor_profile.pan_no = data.get('pan_no')
        vendor_profile.company_registration = data.get('company_registration')
        vendor_profile.registered_year = data.get('registered_year')

        user_data=data.get('user')
        user = vendor_profile.user
        user.full_name = user_data.get('full_name')
        user.phonenumber = user_data.get('phonenumber')
        user.address = user_data.get('address')
        user.dateofbirth = user_data.get('dateofbirth')
        user.gender = user_data.get('gender')
        user.occupation = user_data.get('occupation')
        user.citizenship_number = user_data.get('citizenship_number')
        user.nid_number = user_data.get('nid_number')
        user.issued_date = user_data.get('issued_date')
        user.issued_district = user_data.get('issued_district')
        user.citizenship_front = user_data.get('citizenship_front')
        user.citizenship_back = user_data.get('citizenship_back')

        vendor_profile.save()
        user.save()
        return Response({'detail': 'Profile updated successfully','Data':VendorProfileSerializer(vendor_profile).data})
        