from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserSignupView,LoginView,VerifyOTPView,UserProfileView,VendorProfileView,ChangePasswordView,PasswordResetView,PasswordResetConfirmView,KYCVerificationView,DeleteAccountView,GetUserView

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('change-password/',ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('vendor-profile/', VendorProfileView.as_view(), name='vendor-profile'),
    path('verify-kyc/', KYCVerificationView.as_view(), name='verify-kyc'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    
]
