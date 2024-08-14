from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Vehicle
from .serializers import VehicleSerializer
# Create your views here.

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def create(self, request, *args, **kwargs):
        vendor = request.user
        vehicle_name = request.data.get('vehicle_name')
        vehicle_type = request.data.get('vehicle_type')
        vehicle_image_front = request.data.get('vehicle_image_front')  
        vehicle_image_back = request.data.get('vehicle_image_back')
        vehicle_image_left = request.data.get('vehicle_image_left')
        vehicle_image_right = request.data.get('vehicle_image_right')
        vehicle_image_speedometer = request.data.get('vehicle_image_speedometer')
        price_per_day = request.data.get('price_per_day')
        price_per_week = request.data.get('price_per_week')
        price_per_month = request.data.get('price_per_month')
        bike_condition = request.data.get('bike_condition')
        category = request.data.get('category')
        theft_assurance = request.data.get('theft_assurance')
        distance_travelled = request.data.get('distance_travelled')
        last_service_date = request.data.get('last_service_date')
        power = request.data.get('power')
        duration = request.data.get('duration')
        discount = request.data.get('discount')
        
        vehicle=Vehicle.objects.create(
            vendor=request.user,  
            vehicle_name=vehicle_name,
            vehicle_type=vehicle_type,
            vehicle_image_front=vehicle_image_front,
            vehicle_image_back=vehicle_image_back,
            vehicle_image_left=vehicle_image_left,
            vehicle_image_right=vehicle_image_right,
            vehicle_image_speedometer=vehicle_image_speedometer,
            price_per_day=price_per_day,
            price_per_week=price_per_week,
            price_per_month=price_per_month,
            bike_condition=bike_condition,
            category=category,
            theft_assurance=theft_assurance,
            distance_travelled=distance_travelled,
            last_service_date=last_service_date,
            power=power,
            duration=duration,
            discount=discount

        )
        vehicle.save()
        return Response({'Message':'Vehicle Added'})

class VehicleEditView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def patch(self, request, *args, **kwargs):
        
        vehicle=self.get_object()
        data=request.data

        for field,new_value in data.items():
            if hasattr(vehicle,field):
                setattr(vehicle,field,new_value)
                vehicle.save()
                return Response({'Message':f'Field {field} updated to {new_value} successfully'})
            else:
                return Response({'Message':f'Field {field} does not exist'})
        vehicle.save()
       

        