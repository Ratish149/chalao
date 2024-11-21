from django.urls import path
from .views import *

urlpatterns = [
    path('vehicle/', VehicleListCreateView.as_view(), name='vehicle'),
    path('vehicle/?vehicle_name=vehicle_name&vehicle_type=bike/scooter/electric&fuel_type=fuel_type&bike_condition=1-5&category=budget&theft_assurance=covered/not_covered&distance_travelled&duration=day/week/month/year/all&power_min&power_max', VehicleListCreateView.as_view(), name='vehicle_filter'),
    path('vehicle/<int:pk>/', VehicleEditView.as_view(), name='vehicle-edit'),
    path('booking/', BookingListCreateView.as_view(), name='booking'),
    path('booking/upload-images/', BookingImageUploadView.as_view(), name='upload-images'),
    path('booking/verify-booking/<int:pk>', BookingVerifyView.as_view(), name='verify-booking'),
    path('extend-booking/<int:pk>', ExtendBookingView.as_view(), name='extend-booking'),
    path('cancel-booking/<int:pk>', CancelBookingView.as_view(), name='cancel-booking'),
    
    path('promo-codes/', PromoCodeListCreateView.as_view(), name='promo-code-list-create'),
    path('promo-codes/validate/', PromoCodeValidateApplyView.as_view(), name='promo-code-validate'),
    path('favorite-vehicle/', FavoriteVehicleListCreateView.as_view(), name='favourite-list-create'),
    path('favorite-vehicle/<int:vehicle_id>/', FavoriteVehicleDetailView.as_view(), name='favorite-vehicle-detail'),
]
