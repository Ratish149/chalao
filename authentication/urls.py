from django.urls import path
from .views import UserSignupView,LoginView
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
]
