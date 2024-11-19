from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Vehicle,FavoriteVehicle,Booking,BookingImages,ExtendBooking,CancelBooking,VehicleReview,PromoCode
from .serializers import VehicleSerializer,FavouriteVehicleSerializer,BookingSerializer,BookingImagesSerializer,ExtendBookingSerializer,VehicleReviewSerializer,PromoCodeSerializer,ValidatePromoCodeSerializer
from rest_framework.exceptions import ValidationError
import json

# Create your views here.

class VehicleListCreateView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)

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
        fuel_type = request.query_params.get('fuel_type', None) 

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

        if fuel_type:  # Add filter for fuel_type
            filters &= Q(fuel_type__icontains=fuel_type)

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
        price = request.data.get('price', {})
        price_data = json.loads(price)
        
        vehicle=Vehicle.objects.create(
            vendor=vendor,  
            vehicle_name=vehicle_name,
            vehicle_type=vehicle_type,
            thumbnail_image=thumbnail_image,
            price=price_data,
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

        vehicle.save()
        return Response({'Message':'Vehicle Added'})


class VehicleEditView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def patch(self, request, *args, **kwargs):
        try:
            vehicle = self.get_object()
            vendor = request.user
            
            # Check if the vendor is the owner of the vehicle
            if vehicle.vendor != vendor:
                return Response({'error': 'Permission Denied: You are not the owner of this vehicle'}, status=403)

            data = request.data
            print(data)
            
            # Update Vehicle fields based on the Vehicle model
            vehicle.vehicle_name = data.get('vehicle_name', vehicle.vehicle_name)
            vehicle.vehicle_type = data.get('vehicle_type', vehicle.vehicle_type)
            vehicle.thumbnail_image = data.get('thumbnail_image', vehicle.thumbnail_image)
            vehicle.bike_condition = data.get('bike_condition', vehicle.bike_condition)
            vehicle.category = data.get('category', vehicle.category)
            vehicle.theft_assurance = data.get('theft_assurance', vehicle.theft_assurance)
            vehicle.chassis_number = data.get('chassis_number', vehicle.chassis_number)
            vehicle.registration_number = data.get('registration_number', vehicle.registration_number)
            vehicle.insurance_number = data.get('insurance_number', vehicle.insurance_number)
            vehicle.engine_number = data.get('engine_number', vehicle.engine_number)
            vehicle.price = json.loads(data.get('price', vehicle.price)) 
            vehicle.distance_travelled = data.get('distance_travelled', vehicle.distance_travelled)
            vehicle.last_service_date = data.get('last_service_date', vehicle.last_service_date)
            vehicle.next_service_date = data.get('next_service_date', vehicle.next_service_date)
            vehicle.next_service_distance = data.get('next_service_distance', vehicle.next_service_distance)
            vehicle.power = data.get('power', vehicle.power)
            vehicle.duration = data.get('duration', vehicle.duration)
            vehicle.discount = data.get('discount', vehicle.discount)
            vehicle.available = data.get('available', vehicle.available)
            vehicle.vendor=vendor

            # Handle file uploads for Vehicle
            if 'thumbnail_image' in request.FILES:
                vehicle.thumbnail_image = request.FILES['thumbnail_image']
            
            vehicle.save()
            return Response({'Message': 'Vehicle updated successfully'})

        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=404)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=500)

class FavouriteVehicleListCreateView(ListCreateAPIView):
    serializer_class=FavouriteVehicleSerializer

    def get_queryset(self):
        return FavoriteVehicle.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Message':'Please Login First'})
        
        vehicle_id=request.data.get('vehicle_id')
        vehicle=Vehicle.objects.get(id=vehicle_id)
        if FavoriteVehicle.objects.filter(user=request.user,vehicle=vehicle).exists():
            return Response({'Message':'Vehicle already added to favourites'})
        favorite_vehicle=FavoriteVehicle.objects.create(user=request.user,vehicle=vehicle)
        favorite_vehicle.save()
        return Response({'Message':'Vehicle added to favourites'})
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Message': 'Please Login First'}, status=status.HTTP_401_UNAUTHORIZED)

        vehicle_id = request.data.get('vehicle_id')
        try:
            favorite_vehicle = FavoriteVehicle.objects.get(user=request.user, vehicle_id=vehicle_id)
            favorite_vehicle.delete()
            return Response({'Message': 'Vehicle removed from favourites'})
        except FavoriteVehicle.DoesNotExist:
            return Response({'Message': 'Vehicle not found in favourites'}, status=status.HTTP_404_NOT_FOUND)


class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.filter(cancel_status=False)
    serializer_class = BookingSerializer  

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # Check if the user is authenticated
            return Response({'Message': 'Please Login First'}, status=status.HTTP_401_UNAUTHORIZED)  # Return 401 Unauthorized

        user = request.user
        bookings = Booking.objects.filter(user=user, cancel_status=False)  # Get all bookings for the authenticated user
        booking_serializer = self.get_serializer(bookings, many=True)

        # Prepare the response to include vehicle data within each booking
        response_data = []
        for booking, booking_data in zip(bookings, booking_serializer.data):  # Use zip to iterate over both
            vehicle_data = VehicleSerializer(booking.vehicle).data  # Serialize the associated vehicle
            booking_data['vehicle'] = vehicle_data  # Add vehicle data to the booking data
            response_data.append(booking_data)
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Message':'Please Login First'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = request.user
        vehicle_id = request.data.get('vehicle_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        city = request.data.get('city')
        pickup_location = request.data.get('pickup_location')
        total_price = request.data.get('total_price')
        payment_method = request.data.get('payment_method')
        promo_code = request.data.get('promo_code')

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            
            # Check if promo_code is provided before trying to get it
            if promo_code:
                promocode = PromoCode.objects.get(code=promo_code)
            else:
                promocode = None  # Set to None if no promo code is provided

            if vehicle.available:
                vehicle.is_booked = True
                vehicle.available = False
                vehicle.save()
            
            booking = Booking.objects.create(
                user=user,
                vehicle=vehicle,
                start_date=start_date,
                end_date=end_date,
                city=city,
                pickup_location=pickup_location,
                total_price=total_price,
                payment_method=payment_method,
                promo_code=promocode  # This can be None if no promo code was provided
            )
            booking.save()
            return Response({'Message': 'Booking Confirmed'})

        except Vehicle.DoesNotExist:
            return Response({'Message': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
        except PromoCode.DoesNotExist:
            # This block will only execute if promo_code was provided but is invalid
            if promo_code:  # Only return this error if a promo code was actually provided
                return Response({'Message': 'Promo code not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Message': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookingImageUploadView(ListCreateAPIView):
    queryset = BookingImages.objects.filter()
    serializer_class= BookingImagesSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)

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
            booking.vehicle.save()
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

class PromoCodeListCreateView(ListCreateAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

class PromoCodeApplyView(GenericAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = ValidatePromoCodeSerializer

    def post(self, request, *args, **kwargs):
        promo_code = request.data.get('promo_code')  # Get the promo code from the request data
        
        try:
            promo = PromoCode.objects.get(code=promo_code)  # Retrieve the promo code object
            
            if not promo.is_valid():
                return Response({
                    'message': 'This promo code is expired or has reached maximum uses.'
                }, status=status.HTTP_400_BAD_REQUEST)

            promo.current_uses += 1
            promo.save()

            return Response({
                'message': 'Promo code applied successfully',
                'discount_percent': promo.discount_percent
            })
        
        except PromoCode.DoesNotExist:
            return Response({
                'message': 'Invalid promo code'
            }, status=status.HTTP_404_NOT_FOUND)

class PromoCodeValidateView(GenericAPIView):
    serializer_class = ValidatePromoCodeSerializer

    def post(self, request):
        promo_code = request.data.get('promo_code')  # Get the promo code from the request data
        
        if not promo_code:
            return Response({
                'valid': False,
                'message': 'Promo code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        print(promo_code)

        try:
            promo = PromoCode.objects.get(
                code=promo_code,
                is_active=True
            )
            
            if not promo.is_valid():
                return Response({
                    'valid': False,
                    'message': 'This promo code is expired or has reached maximum uses.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'valid': True,
                'discount_percent': promo.discount_percent,
                'message': 'Promo code is valid'
            })

        except PromoCode.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'Invalid promo code'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log the exception for debugging
            print(f"Unexpected error: {str(e)}")
            return Response({
                'valid': False,
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
