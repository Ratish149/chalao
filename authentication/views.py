from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,GenericAPIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .serializers import UserSignupSerializer,LoginSerializer
from django.contrib.auth import authenticate
from .models import User

# Create your views here.

class UserSignupView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
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
               

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username=request.data.get('username')
        password=request.data.get('password')
        otp = request.data.get('otp')

        user=authenticate(username=username,password=password)

        if user is not None:
            if user.otp == otp:
                user.otp=''
                user.is_verified=True
                user.save()
                return Response({'Message':'Login Successful'})
            else:
                return Response({'Message':'OTP Failed'})
        else:
            return Response({'Message':'Login Failed'})