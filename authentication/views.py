from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
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

        email=request.data.get('email')
        username=email.split('@')[0]
        password=request.data.get('password')
        confirm_password=request.data.get('confirm_password')
        user_type=request.data.get('user_type')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists'})
            elif User.objects.filter(email=email).exists():
                return Response({'detail': 'Email already exists'})
            else:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type=user_type
                )
        else:
            return Response({'detail': 'password and confirm password do not match'})

        otp = get_random_string(length=6,allowed_chars='0123456789')
        user.otp = otp
        user.save()
        
        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            'bdevil149@gmail.com',
            ['ratish.shakya149@gmail.com',user.email],
            fail_silently=False,
        )
        if user.user_type == 'VENDOR':
            VendorProfile.objects.create(user=user)
        elif user.user_type == 'USER':
            UserProfile.objects.create(user=user)

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

        if '@' in username:
            username=username.split('@')[0]

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_verfied:
                return Response({'Message':'Login Successful!'})
            else:
                return Response({'Message':'Email not verified'})
        else:
            return Response({'Message':'Login Failed'})
        
class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        data = request.data

        user_profile.license_number = data.get('license_number', user_profile.license_number)
        user_profile.expiry_date = data.get('expiry_date', user_profile.expiry_date)
        user_profile.issued_district = data.get('issued_district', user_profile.issued_district)
        
        if 'driving_license_front' in request.FILES:
            user_profile.driving_license_front = request.FILES['driving_license_front']
        if 'driving_license_back' in request.FILES:
            user_profile.driving_license_back = request.FILES['driving_license_back']

        user_data = data.get('user', {})
        user = user_profile.user

        user.full_name = user_data.get('full_name', user.full_name)
        user.phonenumber = user_data.get('phonenumber', user.phonenumber)
        user.address = user_data.get('address', user.address)
        user.dateofbirth = user_data.get('dateofbirth', user.dateofbirth)
        user.gender = user_data.get('gender', user.gender)
        user.occupation = user_data.get('occupation', user.occupation)
        user.citizenship_number = user_data.get('citizenship_number', user.citizenship_number)
        user.nid_number = user_data.get('nid_number', user.nid_number)
        user.issued_date = user_data.get('issued_date', user.issued_date)
        user.issued_district = user_data.get('issued_district', user.issued_district)

        if 'citizenship_front' in request.FILES:
            user.citizenship_front = request.FILES['citizenship_front']
        if 'citizenship_back' in request.FILES:
            user.citizenship_back = request.FILES['citizenship_back']

        user_profile.save()
        user.save()

        return Response({'detail': 'Profile updated successfully', 'Data': UserProfileSerializer(user_profile).data})

class VendorProfileView(RetrieveUpdateAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    def get(self, request, *args, **kwargs):
        vendor_profile = VendorProfile.objects.get(user=request.user)
        serializer = VendorProfileSerializer(vendor_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        vendor_profile = VendorProfile.objects.get(user=self.request.user)
        data=request.data

        vendor_profile.pan_no = data.get('pan_no')
        vendor_profile.registered_year = data.get('registered_year')
        if 'company_registration' in request.FILES:
            vendor_profile.company_registration = request.FILES['company_registration']

        user_data=data.get('user')
        user = vendor_profile.user

        user.full_name = user_data.get('full_name', user.full_name)
        user.phonenumber = user_data.get('phonenumber', user.phonenumber)
        user.address = user_data.get('address', user.address)
        user.dateofbirth = user_data.get('dateofbirth', user.dateofbirth)
        user.gender = user_data.get('gender', user.gender)
        user.occupation = user_data.get('occupation', user.occupation)
        user.citizenship_number = user_data.get('citizenship_number', user.citizenship_number)
        user.nid_number = user_data.get('nid_number', user.nid_number)
        user.issued_date = user_data.get('issued_date', user.issued_date)
        user.issued_district = user_data.get('issued_district', user.issued_district)

        if 'citizenship_front' in request.FILES:
            user.citizenship_front = request.FILES['citizenship_front']
        if 'citizenship_back' in request.FILES:
            user.citizenship_back = request.FILES['citizenship_back']

        vendor_profile.save()
        user.save()
        return Response({'detail': 'Profile updated successfully','Data':VendorProfileSerializer(vendor_profile).data})
        