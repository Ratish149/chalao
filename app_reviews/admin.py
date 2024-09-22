from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AppReview
# Register your models here.

admin.site.register(AppReview, ModelAdmin)