from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Vehicle
from .serializers import VehicleSerializer
# Create your views here.

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer