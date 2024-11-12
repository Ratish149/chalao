from django.shortcuts import render
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Vehicle,Price,Booking,BookingImages,ExtendBooking,CancelBooking,VehicleReview
from .serializers import VehicleSerializer,BookingSerializer,BookingImagesSerializer,PriceSerializer,ExtendBookingSerializer,VehicleReviewSerializer

# Create your views here.

class VehicleListCreateView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        user_city = self.request.query_params.get('user_city', None)  # Get user city from query params
        
        # If user is authenticated and is a vendor, return their vehicles
        if user.is_authenticated and user.user_type == 'VENDOR':
            return Vehicle.objects.filter(vendor=user,available=True)
        
        # If user_city is provided, filter vehicles based on vendor's city
        if user_city:
            return Vehicle.objects.filter(vendor__vendorprofile__city=user_city,available=True)  # Assuming vendor has a related VendorProfile
        
        # If no user_city is provided, return all vehicles
        return Vehicle.objects.filter(available=True)

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        filters = Q(available=True)

        vehicle_name = request.query_params.get('vehicle_name', None)
        vehicle_type = request.query_params.get('vehicle_type', None)
        
        category = request.query_params.get('category', None)
        bike_condition = request.query_params.get('bike_condition', None)
        theft_assurance = request.query_params.get('theft_assurance', None)
        distance_travelled = request.query_params.get('distance_travelled', None)
        duration = request.query_params.get('duration', None)
        power_min = request.query_params.get('power_min', None)
        power_max = request.query_params.get('power_max', None)

        if vehicle_name:
            filters &= Q(vehicle_name__icontains=vehicle_name)

        if vehicle_type:
            filters &= Q(vehicle_type__icontains=vehicle_type)

        if category:
            filters &= Q(category__icontains=category)

        if bike_condition:
            filters &= Q(bike_condition__icontains=bike_condition)

        if theft_assurance:
            filters &= Q(theft_assurance__icontains=theft_assurance)

        if distance_travelled:
            filters &= Q(distance_travelled__icontains=distance_travelled)

        if duration:
            filters &= Q(duration__icontains=duration)

        if power_min is not None and power_max is not None:
            filters &= Q(power__range=(power_min, power_max))
        elif power_min is not None:
            filters &= Q(power__gte=power_min)
        elif power_max is not None:
            filters &= Q(power__lte=power_max)

        filtered_queryset = queryset.filter(filters)

        if not filtered_queryset.exists():
            return Response({'Message': 'No vehicles found matching the provided filters'})

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        
        vendor = request.user

        vehicle_name = request.data.get('vehicle_name')
        vehicle_type = request.data.get('vehicle_type')
        thumbnail_image=request.data.get('thumbnail_image')

        chassis_number = request.data.get('chassis_number')
        registration_number = request.data.get('registration_number')
        insurance_number = request.data.get('insurance_number')
        engine_number = request.data.get('engine_number')

        bike_condition = request.data.get('bike_condition')
        category = request.data.get('category')
        theft_assurance = request.data.get('theft_assurance')
        distance_travelled = request.data.get('distance_travelled')
        last_service_date = request.data.get('last_service_date')
        next_service_date = request.data.get('next_service_date')
        next_service_distance = request.data.get('next_service_distance')
        power = request.data.get('power')
        duration = request.data.get('duration')
        discount = request.data.get('discount')
        
        vehicle=Vehicle.objects.create(
            vendor=vendor,  
            vehicle_name=vehicle_name,
            vehicle_type=vehicle_type,
            thumbnail_image=thumbnail_image,
            chassis_number=chassis_number,
            registration_number=registration_number,
            insurance_number=insurance_number,
            engine_number=engine_number,
            bike_condition=bike_condition,
            category=category,
            theft_assurance=theft_assurance,
            distance_travelled=distance_travelled,
            last_service_date=last_service_date,
            next_service_date=next_service_date,
            next_service_distance=next_service_distance,
            power=power,
            duration=duration,
            discount=discount
        )

        price=Price.objects.create(
            vehicle=vehicle,
            duration=duration,
            price=discount
        )
        price.save()
        vehicle.save()
        return Response({'Message':'Vehicle Added'})
class PriceListCreateView(ListCreateAPIView):
    # queryset = Price.objects.all()
    serializer_class = PriceSerializer
    def get_queryset(self):
        return Price.objects.filter(vehicle__vendor=self.request.user)

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
    queryset = Booking.objects.filter(cancel_status=False)
    serializer_class = BookingSerializer  

    def get(self, request, *args, **kwargs):
        user = request.user
        bookings = Booking.objects.filter(user=user, cancel_status=False)  # Get all bookings for the authenticated user
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

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
            vehicle.available=False
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
    queryset = BookingImages.objects.filter()
    serializer_class= BookingImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

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
             

class ExtendBookingView(ListCreateAPIView):
    queryset = ExtendBooking.objects.all()
    serializer_class = ExtendBookingSerializer

    def get(self, request, *args, **kwargs):

        booking_id = self.kwargs.get('pk')
        try:

            extend_booking = ExtendBooking.objects.get(
                booking__id=booking_id,
                booking__user=request.user
            )
        except:
            return Response({'Message': 'ExtendBooking not found or does not belong to the user'})

        serializer = self.get_serializer(extend_booking)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        booking_id = self.kwargs.get('pk') 
        booking=Booking.objects.get(id=booking_id, user=self.request.user)
        if request.user != booking.user:
            return Response({'Message': 'Permission Denied'})
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        price = request.data.get('price')
        remarks = request.data.get('remarks', '')
        booking.end_date = end_date

        extend_booking = ExtendBooking.objects.create(
            booking=booking,
            start_date=start_date,
            end_date=end_date,
            price=price,
            remarks=remarks
        )
        booking.save()
        extend_booking.save()

        return Response({'Data': ExtendBookingSerializer(extend_booking).data,'Message': 'Booking Extended Successfully'})

class CancelBookingView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        remarks = request.data.get('remarks', None)

        if request.user == booking.user or request.user == booking.vehicle.vendor:
            booking.cancel_status = True
            booking.vehicle.available = True
            booking.save()           
            CancelBooking.objects.create(
                    booking=booking,
                    remarks=remarks
            )
            return Response({'Message': 'Booking Cancelled'})
        else:
            return Response({'Message': 'Permission Denied'})

class VehicleReviewListView(ListCreateAPIView):
    queryset = VehicleReview.objects.all()
    serializer_class = VehicleReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vehicle_id = self.kwargs.get('pk')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle_reviews = VehicleReview.objects.filter(vehicle=vehicle)
        serializer = self.get_serializer(vehicle_reviews, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Message':'Please Login First'})
        
        user=request.user
        vehicle_id=request.data.get('vehicle_id')
        rating=request.data.get('rating')
        comment=request.data.get('comment')
        vehicle=Vehicle.objects.get(id=vehicle_id)
        vehicle_review = VehicleReview.objects.create(
            user=user,
            vehicle=vehicle,
            rating=rating,
            review=comment
        )
        vehicle_review.save()
        serializer = self.get_serializer(vehicle_review)
        return Response(serializer.data)

class VehicleReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleReview.objects.all()
    serializer_class = VehicleReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review_id = self.kwargs.get('pk')
        return get_object_or_404(VehicleReview, id=review_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'Message': 'You are not authorized to update this review'}, status=status.HTTP_403_FORBIDDEN)
        
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        
        if rating is not None:
            instance.rating = rating
        if comment is not None:
            instance.comment = comment
        
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'Message': 'You are not authorized to delete this review'}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({'Message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
