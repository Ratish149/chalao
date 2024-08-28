from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView,GenericAPIView,RetrieveUpdateAPIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer,LoginSerializer,UserProfileSerializer,VendorProfileSerializer,ChangePasswordSerializer,VerifyOTPSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer,KYCVerificationSerializer
from django.contrib.auth import authenticate
from .models import User,UserProfile,VendorProfile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserSignupView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            full_name=request.data.get('full_name')
            phonenumber=request.data.get('phone_number')
            email=request.data.get('email')
            username=email.split('@')[0]
            password=request.data.get('password')
            confirm_password=request.data.get('confirm_password')
            user_type=request.data.get('user_type')

            if password != confirm_password:
                return Response({'detail': 'Password and confirm password do not match'})
            
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists'})
            elif User.objects.filter(email=email).exists():
                return Response({'detail': 'Email already exists'})
            elif User.objects.filter(phonenumber=phonenumber).exists():
                return Response({'detail': 'Phone number already exists'})
            
            user=User.objects.create_user(
                full_name=full_name,
                phonenumber=phonenumber,
                username=username,
                email=email,
                password=password,
                user_type=user_type
            )
            
            otp = get_random_string(length=6,allowed_chars='0123456789')
            user.otp = otp
            user.save()
            try:
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp}',
                    'bdevil149@gmail.com',
                    ['ratish.shakya149@gmail.com',user.email],
                    fail_silently=False,
                )
            except:
                return Response({'detail': 'Failed to send OTP'})
            
            if user.user_type == 'VENDOR':
                VendorProfile.objects.create(user=user)
            elif user.user_type == 'USER':
                UserProfile.objects.create(user=user)

            token=get_tokens_for_user(user)
            return Response(
                        {
                        "token":token
                    })
        except Exception as e:
            return Response({'detail': str(e)})

class VerifyOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer
   
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
        login_field=request.data.get('c')
        password=request.data.get('password')
        try:
            if '@' in login_field:
                user=User.objects.get(email=login_field)
                # username=username.split('@')[0]
            elif login_field.isdigit():
                user=User.objects.get(phonenumber=login_field)
            else:
                user=User.objects.get(username=login_field)
        except User.DoesNotExist:
            return Response({'Message':'User does not exist'})
        
        user = authenticate(username=user.username, password=password)

        if user is not None:
            if user.is_verified:
                token=get_tokens_for_user(user)
                return Response(
                    {
                    'Message':'Login Successful!',
                    "token":token                    
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

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self,request,*args, **kwargs):
        email=request.data.get('email')

        if not email:
            return Response({'detail': 'Email is required'})

        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'})
        
        token=default_token_generator.make_token(user)
        # user.token=token
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        reset_link= f'http://localhost:3000/reset-password/?uid={uid}&token={token}'

        subject = 'Password Reset Link'
        message=f'Click the following link to reset your password: {reset_link}'

        try:
            send_mail(
                subject,
                message,
                'bdevil149@gmail.com',
                ['ratish.shakya149@gmail.com',email],
                fail_silently=False,
            )
            return Response({'detail': 'Password reset link sent to your email'})
        except:
            return Response({'detail': 'Failed to send password reset link'})

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not uid or not token or not new_password:
            return Response({'detail': 'UID, token, and new password are required'})
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid user ID or token'})

        if default_token_generator.check_token(user, token):   
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful'})
        else:
            return Response({'detail': 'Invalid or expired token'})

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
            
            vendor_profile.pan_no = data.get('pan_no', vendor_profile.pan_no)
            vendor_profile.registered_year = data.get('registered_year', vendor_profile.registered_year)
            
            if 'company_registration' in request.FILES:
                vendor_profile.company_registration = request.FILES['company_registration']
            
            user = vendor_profile.user
            user_fields = ['full_name', 'phonenumber', 'address', 'dateofbirth', 'gender', 
                           'occupation', 'citizenship_number', 'nid_number', 'issued_date', 'issued_district']
            
            for field in user_fields:
                key = f'user[{field}]'
                if key in data:
                    setattr(user, field, data[key])
            
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
        
class KYCVerificationView(GenericAPIView):
    serializer_class = KYCVerificationSerializer
    def post(self, request, *args, **kwargs):
        user_id=request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'User ID is required'})
               
        user=User.objects.get(id=user_id)
        if not user.kyc_verified:
            user.kyc_verified=True
            user.save()
            return Response({'detail': 'KYC verification successful'})
        else:
            return Response({'detail': 'KYC already verified'})