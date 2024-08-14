from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,GenericAPIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer,LoginSerializer
from django.contrib.auth import authenticate
from .models import User

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
        # otp = request.data.get('otp')

        user=authenticate(username=username,password=password)

        if user is not None:
            if user.is_verfied:
                return Response({'Message':'Login Successful!'})
            else:
                return Response({'Message':'OTP Failed'})
        else:
            return Response({'Message':'Login Failed'})