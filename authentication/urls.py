from django.urls import path
from .views import UserSignupView,LoginView,VerifyOTPView
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

]
