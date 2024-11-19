from rest_framework import serializers
from .models import Vehicle,FavoriteVehicle,Booking,BookingImages,ExtendBooking,CancelBooking,VehicleReview,PromoCode



class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

class FavouriteVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=FavoriteVehicle
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','vehicle','start_date','end_date','city','pickup_location','total_price','payment_method','promo_code']

class BookingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingImages
        fields = '__all__'

class ExtendBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendBooking
        fields = '__all__'

class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelBooking
        fields = '__all__'

class VehicleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleReview
        fields = '__all__'

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
        read_only_fields = ('current_uses', 'created_at', 'updated_at')

class ValidatePromoCodeSerializer(serializers.Serializer):
    promo_code = serializers.CharField(max_length=50)