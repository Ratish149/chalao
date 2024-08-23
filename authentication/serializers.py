from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import VendorProfile,UserProfile

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('email','password','user_type')
        extra_kwargs = {
            'password': {'write_only': True},
        }
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    token=serializers.CharField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = [
            'full_name',
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
            
            ]
class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'user',
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
            'company_registration',
            'registered_year',
        ]

