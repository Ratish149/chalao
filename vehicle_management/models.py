from django.db import models

# Create your models here.

class Vehicle(models.Model):
    TYPE={
        'BIKE':'BIKE',
        'SCOOTER':'SCOOTER',
        'ELETRIC':'ELETRIC',
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

    vendor = models.ForeignKey('authentication.User',on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100,choices=TYPE)
    
    vehicle_image_front = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_back = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_left = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_right = models.ImageField(upload_to='vehicle',blank=True,null=True)
    vehicle_image_speedometer = models.ImageField(upload_to='vehicle',blank=True,null=True)

    price_per_day = models.IntegerField(blank=True,null=True)
    price_per_week = models.IntegerField(blank=True,null=True)
    price_per_month = models.IntegerField(blank=True,null=True)

    bike_condition=models.CharField(max_length=100,blank=True,null=True)
    category=models.CharField(max_length=100,blank=True,null=True)
    theft_assurance=models.CharField(max_length=100,choices=THEFT_ASSURANCE)
    distance_travelled=models.IntegerField(blank=True,null=True)
    last_service_date=models.DateField(blank=True,null=True)
    power = models.IntegerField(blank=True,null=True)
    duration=models.CharField(max_length=100,choices=DURATION)
    discount = models.IntegerField(blank=True,null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_name