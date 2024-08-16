from django.contrib import admin
from .models import Price,Vehicle,Booking,BookingImages
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(Price, ModelAdmin)
admin.site.register(Vehicle,ModelAdmin)
admin.site.register(Booking, ModelAdmin)
admin.site.register(BookingImages, ModelAdmin)