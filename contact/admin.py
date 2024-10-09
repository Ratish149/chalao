from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Contact

# Register your models here.
admin.site.register(Contact, ModelAdmin)
