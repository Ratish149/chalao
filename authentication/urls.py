from django.urls import path
from .views import UserSignupView,LoginView,VerifyOTPView,UserProfileView,VendorProfileView,ChangePasswordView
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('change-password/',ChangePasswordView.as_view(), name='change-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('vendor-profile/', VendorProfileView.as_view(), name='vendor-profile'),

]
