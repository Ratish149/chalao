from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import VendorProfile,UserProfile

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('full_name','phonenumber','email','password','user_type')
        extra_kwargs = {
            'password': {'write_only': True},
        }
class VerifyOTPSerializer(serializers.Serializer):
    otp=serializers.CharField(max_length=6)
    
class LoginSerializer(serializers.Serializer):
    login_field = serializers.CharField()
    password = serializers.CharField()
    token=serializers.CharField(read_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(write_only=True,required=True)
    new_password=serializers.CharField(write_only=True,required=True)

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.CharField(write_only=True, required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    email=serializers.CharField()
    otp=serializers.CharField()
    new_password=serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = [
            'id',
            'user_type',
            'full_name',
            'profile_picture',
            'phonenumber',
            'address',
            'dateofbirth',
            'gender',
            'occupation',
            'citizenship_number',
            'nid_number',
            'issued_date',
            'issued_district',
            'citizenship_front',
            'citizenship_back',
            'kyc_verified',
            
            ]
class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'user_image_top',
            'user_image_left',
            'user_image_right',
            'license_number',
            'expiry_date',
            'issued_district',
            'driving_license_front',
            'driving_license_back',
        ]

class VendorProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = VendorProfile
        fields = [
            'user',
            'pan_no',
            'pan_no_image',
            'vat_no',
            'vat_no_image',
            'company_registration',
            'registered_year',
        ]

class KYCVerificationSerializer(serializers.Serializer):
    user_id=serializers.IntegerField()