from django.contrib import admin
from .models import Vehicle,Booking,BookingImages,ExtendBooking,CancelBooking,VehicleReview,PromoCode,FavoriteVehicle
from unfold.admin import ModelAdmin
# Register your models here.

# admin.site.register(Price, ModelAdmin)
admin.site.register(Vehicle,ModelAdmin)
admin.site.register(Booking, ModelAdmin)
admin.site.register(BookingImages, ModelAdmin)
admin.site.register(ExtendBooking, ModelAdmin)
admin.site.register(CancelBooking, ModelAdmin)
admin.site.register(VehicleReview, ModelAdmin)
admin.site.register(PromoCode, ModelAdmin)
admin.site.register(FavoriteVehicle, ModelAdmin)