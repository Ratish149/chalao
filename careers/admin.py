from django.contrib import admin
from unfold.admin import ModelAdmin
from django.db import models
from .models import Job,JobApplications
from tinymce.widgets import TinyMCE

class JobAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE,},
    }

admin.site.register(Job, JobAdmin)
admin.site.register(JobApplications, ModelAdmin)