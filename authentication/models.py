from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE={
        'VENDOR':'VENDOR',
        'USER':'USER',
    }
    user_type=models.CharField(max_length=10,choices=USER_TYPE)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    citizenship_front=models.ImageField(upload_to='citizenship')
    citizenship_back=models.ImageField(upload_to='citizenship')
    driving_license=models.ImageField(upload_to='driving_license')

    def __str__(self):
        return self.user.username

class VendorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    pan_no=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.user.username

