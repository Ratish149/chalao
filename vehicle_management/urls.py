from django.urls import path
from .views import *

urlpatterns = [
    path('vehicle/', VehicleListCreateView.as_view(), name='vehicle'),
    path('vehicle/<int:pk>/', VehicleEditView.as_view(), name='vehicle-edit'),
    path('booking/', BookingListCreateView.as_view(), name='booking'),
    path('booking/upload-images/', BookingImageUploadView.as_view(), name='upload-images'),
    path('booking/verify-booking/<int:pk>', BookingVerifyView.as_view(), name='verify-booking'),
]
