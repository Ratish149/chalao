from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Vehicle,Price,Booking,BookingImages
from .serializers import VehicleSerializer,BookingSerializer,BookingImagesSerializer
# Create your views here.

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        
        vendor = request.user

        vehicle_name = request.data.get('vehicle_name')
        vehicle_type = request.data.get('vehicle_type')
        thumbnail_image=request.data.get('thumbnail_image')

        price_id=request.data.getlist('price')

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
            thumbnail_image=thumbnail_image,
            bike_condition=bike_condition,
            category=category,
            theft_assurance=theft_assurance,
            distance_travelled=distance_travelled,
            last_service_date=last_service_date,
            power=power,
            duration=duration,
            discount=discount
        )
        if price_id:
            prices=Price.objects.filter(id__in=price_id)
            vehicle.price.set(prices)
            
        vehicle.save()
        return Response({'Message':'Vehicle Added'})

class VehicleEditView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)

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

class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Message':'Please Login First'})
        
        user=request.user
        vehicle_id=request.data.get('vehicle_id')
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')
        city=request.data.get('city')
        pickup_location=request.data.get('pickup_location')
        total_price=request.data.get('total_price')
        
        vehicle=Vehicle.objects.get(id=vehicle_id)
        
        if vehicle.available:
            vehicle.is_booked=True
            vehicle.save()
        
        booking = Booking.objects.create(
            user=user,
            vehicle=vehicle,
            start_date=start_date,
            end_date=end_date,
            city=city,
            pickup_location=pickup_location,
            total_price=total_price
        )
        booking.save()
        return Response({'Message':'Booking Confirmed'})

class BookingImageUploadView(ListCreateAPIView):
    queryset = BookingImages.objects.all()
    serializer_class= BookingImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        booking_id=request.data.get('booking_id')
        booking = Booking.objects.get(id=booking_id)

        if booking:
            if request.user != booking.vehicle.vendor:
                return Response({'Message':'Permission Denied'})
            
            vehicle_image_front=request.data.get('vehicle_image_front')
            vehicle_image_back=request.data.get('vehicle_image_back')
            vehicle_image_left=request.data.get('vehicle_image_left')
            vehicle_image_right=request.data.get('vehicle_image_right')
            vehicle_image_speedometer=request.data.get('vehicle_image_speedometer')

            booking_images=BookingImages.objects.create(
                booking=booking,
                vehicle_image_front=vehicle_image_front,
                vehicle_image_back=vehicle_image_back,
                vehicle_image_left=vehicle_image_left,
                vehicle_image_right=vehicle_image_right,
                vehicle_image_speedometer=vehicle_image_speedometer
            )
            booking_images.save()
            return Response({'Message':'Images Uploaded'})
        else:
            return Response({'Message':'Booking Not Found'})

class BookingVerifyView(RetrieveUpdateDestroyAPIView):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer

    def patch(self, request, *args, **kwargs):
        booking=self.get_object()
        if request.user == booking.user:
            booking.user_verified=True
            booking.save()
            return Response({'Message':'Booking Verified by User'})
        elif request.user ==  booking.vehicle.vendor:
            booking.vendor_verified=True
            booking.save()
            return Response({'Message':'Booking Verified by Vendor'})
        else:
            return Response({'Message':'Permission Denied'})
             