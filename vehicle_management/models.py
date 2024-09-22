from typing import Iterable
from django.db import models

# Create your models here.

class Price(models.Model):
    DURATION={
        'DAILY':'DAILY',
        'WEEKLY':'WEEKLY',
        'MONTHLY':'MONTHLY',
    }
    duration=models.CharField(max_length=100,choices=DURATION)
    price=models.IntegerField()
    vehicle=models.ForeignKey('Vehicle',on_delete=models.CASCADE,related_name='prices')

    def __str__(self):
        return f'{self.vehicle.vehicle_name}'

class Vehicle(models.Model):
    TYPE={
        'BIKE':'BIKE',
        'SCOOTER':'SCOOTER',
        'ELETRIC':'ELETRIC',
        'CAB':'CAB'
    }
    DURATION={
        'DAY':'DAY',
        'WEEK':'WEEK',
        'MONTH':'MONTH',
        'YEAR':'YEAR',
        'ALL':'ALL',
    }
    THEFT_ASSURANCE={
        'COVERED':'COVERED',
        'NOT COVERED':'NOT COVERED',
    }
    CATEGORY={
        'BUDGET':'BUDGET',
        'PREMIUM':'PREMIUM',
        'ELETRIC':'ELETRIC',

    }
    CONDITION={
        '1':'1',
        '2':'2',
        '3':'3',
        '4':'4',
        '5':'5',
    }

    vendor = models.ForeignKey('authentication.User',on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100,choices=TYPE)
    thumbnail_image = models.ImageField(upload_to='vehicle',blank=True, null=True)

    bike_condition=models.CharField(max_length=100,choices=CONDITION,blank=True,null=True)
    category=models.CharField(max_length=100,choices=CATEGORY,blank=True,null=True)
    theft_assurance=models.CharField(max_length=100,choices=THEFT_ASSURANCE)
    distance_travelled=models.IntegerField(blank=True,null=True)
    last_service_date=models.DateField(blank=True,null=True)
    date_of_upload = models.DateField(auto_now_add=True)
    power = models.IntegerField(blank=True,null=True)
    duration=models.CharField(max_length=100,choices=DURATION)
    discount = models.IntegerField(blank=True,null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_name
    
    class Meta:
        ordering = [
            '-date_of_upload'
            ]
    
class Booking(models.Model):    
    PAYMENT_METHOD={
        'CASH':'CASH',
        'ESEWA':'ESEWA',
        'CARD':'CARD',
        'OTHER':'OTHER'
    }

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)
    total_price = models.IntegerField()
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD)
    cancel_status = models.BooleanField(default=False)
    user_verified = models.BooleanField(default=False)
    vendor_verified=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + ' - ' + self.vehicle.vehicle_name
    
class BookingImages(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='images')
    vehicle_image_front = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_back = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_left = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_right = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_speedometer = models.ImageField(upload_to='vehicle',blank=True,null=True)

    def __str__(self):
        return self.booking.user.username + ' - ' + self.booking.vehicle.vehicle_name
    
class ExtendBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.booking.user.username + ' - ' + self.booking.vehicle.vehicle_name

class CancelBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.booking.user.username} - {self.booking.vehicle.vehicle_name} - {self.remarks}'
    
class VehicleReview(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} Reviewed on {self.vehicle.vehicle_name}'
    