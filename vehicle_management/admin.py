from django.contrib import admin
from .models import Vehicle
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.register(Vehicle,ModelAdmin)