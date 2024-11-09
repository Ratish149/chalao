from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Advertisement
# Register your models here.

admin.site.register(Advertisement, ModelAdmin)
