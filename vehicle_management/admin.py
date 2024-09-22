from django.contrib import admin
from .models import Price,Vehicle,Booking,BookingImages,ExtendBooking,CancelBooking,VehicleReview
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(Price, ModelAdmin)
admin.site.register(Vehicle,ModelAdmin)
admin.site.register(Booking, ModelAdmin)
admin.site.register(BookingImages, ModelAdmin)
admin.site.register(ExtendBooking, ModelAdmin)
admin.site.register(CancelBooking, ModelAdmin)
admin.site.register(VehicleReview, ModelAdmin)