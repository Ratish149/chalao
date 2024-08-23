from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView,GenericAPIView,RetrieveUpdateAPIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer,LoginSerializer,UserProfileSerializer,VendorProfileSerializer,ChangePasswordSerializer
from django.contrib.auth import authenticate
from .models import User,UserProfile,VendorProfile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
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

        token=get_tokens_for_user(user)
        return Response(
                    {
                    "token":token
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
            if user.is_verified:
                token=get_tokens_for_user(user)
                return Response(
                    {
                    "token":token,
                    'Message':'Login Successful!'
                })
                
            else:
                return Response({'Message':'Email not verified'})
        else:
            return Response({'Message':'Login Failed'})

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'detail': 'Old password and new password are required'})
        
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect'})
        
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully'})
        
class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    
    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            data = request.data
            
            # Update UserProfile fields
            user_profile.license_number = data.get('license_number', user_profile.license_number)
            user_profile.expiry_date = data.get('expiry_date', user_profile.expiry_date)
            user_profile.issued_district = data.get('issued_district', user_profile.issued_district)
            
            # Handle file uploads for UserProfile
            if 'driving_license_front' in request.FILES:
                user_profile.driving_license_front = request.FILES['driving_license_front']
            if 'driving_license_back' in request.FILES:
                user_profile.driving_license_back = request.FILES['driving_license_back']
            
            # Update User fields
            user = user_profile.user
            user_fields = ['full_name', 'phonenumber', 'address', 'dateofbirth', 'gender', 
                           'occupation', 'citizenship_number', 'nid_number', 'issued_date', 'issued_district']
            
            for field in user_fields:
                key = f'user[{field}]'
                if key in data:
                    setattr(user, field, data[key])
            
            # Handle file uploads for User
            if 'user[citizenship_front]' in request.FILES:
                user.citizenship_front = request.FILES['user[citizenship_front]']
            if 'user[citizenship_back]' in request.FILES:
                user.citizenship_back = request.FILES['user[citizenship_back]']
            
            user_profile.save()
            user.save()
            
            return Response({
                'detail': 'Profile updated successfully',
                'Data': UserProfileSerializer(user_profile).data
            })
        
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=500)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()
        
class VendorProfileView(RetrieveUpdateAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()

    def get(self, request, *args, **kwargs):
        vendor_profile = VendorProfile.objects.get(user=request.user)
        serializer = VendorProfileSerializer(vendor_profile)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        try:
            vendor_profile = VendorProfile.objects.get(user=self.request.user)
            data = request.data
            
            # Update VendorProfile fields
            vendor_profile.pan_no = data.get('pan_no', vendor_profile.pan_no)
            vendor_profile.registered_year = data.get('registered_year', vendor_profile.registered_year)
            
            # Handle file upload for VendorProfile
            if 'company_registration' in request.FILES:
                vendor_profile.company_registration = request.FILES['company_registration']
            
            # Update User fields
            user = vendor_profile.user
            user_fields = ['full_name', 'phonenumber', 'address', 'dateofbirth', 'gender', 
                           'occupation', 'citizenship_number', 'nid_number', 'issued_date', 'issued_district']
            
            for field in user_fields:
                key = f'user[{field}]'
                if key in data:
                    setattr(user, field, data[key])
            
            # Handle file uploads for User
            if 'user[citizenship_front]' in request.FILES:
                user.citizenship_front = request.FILES['user[citizenship_front]']
            if 'user[citizenship_back]' in request.FILES:
                user.citizenship_back = request.FILES['user[citizenship_back]']
            
            vendor_profile.save()
            user.save()
            
            return Response({
                'detail': 'Profile updated successfully',
                'Data': VendorProfileSerializer(vendor_profile).data
            })
        
        except VendorProfile.DoesNotExist:
            return Response({'error': 'Vendor profile not found'}, status=404)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=500)