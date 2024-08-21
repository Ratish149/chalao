from rest_framework import serializers
from .models import Vehicle,Booking,Price,BookingImages,ExtendBooking,CancelBooking

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','vehicle','start_date','end_date','city','pickup_location','total_price','payment_method']

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