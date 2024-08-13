from django.urls import path
from .views import *

urlpatterns = [
    path('vehicle/', VehicleListCreateView.as_view(), name='vehicle'),
]
