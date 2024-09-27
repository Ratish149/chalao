from django.contrib import admin
from unfold.admin import ModelAdmin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Blog
# Register your models here.

class BlogAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE,},
    }

admin.site.register(Blog, BlogAdmin)

