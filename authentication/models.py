from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE={
        'VENDOR':'VENDOR',
        'USER':'USER',
    }
    user_type=models.CharField(max_length=10,choices=USER_TYPE)
    profile_picture=models.ImageField(upload_to='profile picture',blank=True,null=True)
    full_name=models.CharField(max_length=100,blank=True,null=True)
    phonenumber=models.CharField(max_length=15,blank=True,null=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    dateofbirth=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    occupation=models.CharField(max_length=100,blank=True,null=True)

    citizenship_number=models.IntegerField(blank=True,null=True)
    nid_number=models.IntegerField(blank=True,null=True)
    issued_date=models.DateField(blank=True,null=True)
    issued_district=models.CharField(max_length=100,blank=True,null=True)
    citizenship_front=models.ImageField(upload_to='citizenship',blank=True,null=True)
    citizenship_back=models.ImageField(upload_to='citizenship',blank=True,null=True)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,blank=True,null=True)
    kyc_verified=models.BooleanField(default=False)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    user_image_top=models.ImageField(upload_to='profile',blank=True,null=True)
    user_image_left=models.ImageField(upload_to='profile',blank=True,null=True)
    user_image_right=models.ImageField(upload_to='profile',blank=True,null=True)
   
    license_number=models.IntegerField(blank=True,null=True)
    expiry_date=models.DateField(blank=True,null=True)
    issued_district=models.CharField(max_length=100,blank=True,null=True)
    driving_license_front=models.ImageField(upload_to='driving_license',blank=True,null=True)
    driving_license_back=models.ImageField(upload_to='driving_license',blank=True,null=True)

    def __str__(self):
        return self.user.username

class VendorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=100,blank=True,null=True)
    pan_no=models.IntegerField(blank=True,null=True)
    pan_no_image=models.ImageField(upload_to='pan_no',blank=True,null=True)
    vat_no=models.IntegerField(blank=True,null=True)
    vat_no_image=models.ImageField(upload_to='vat_no',blank=True,null=True)
    company_registration=models.ImageField(upload_to='company_registration',blank=True,null=True)
    registered_year=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.user.username

