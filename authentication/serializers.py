from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate

from .models import VendorProfile,UserProfile


User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','email','password','user_type')
        # extra_kwargs = {
        #     'password': {'write_only': True},
        # }

    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
        )
        if user.user_type=='VENDOR':
            VendorProfile.objects.create(user=user)
        elif user.user_type=='USER':
            UserProfile.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    