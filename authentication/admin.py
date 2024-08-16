from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.
from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import User, UserProfile, VendorProfile

class UserProfileInline( admin.TabularInline):
    model = UserProfile
    extra = 1

class VendorProfileInline( admin.TabularInline):
    model = VendorProfile
    extra = 1

class UserAdmin(UnfoldModelAdmin, admin.ModelAdmin):
    inlines = []

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            if obj.user_type == 'VENDOR':
                inline_instances.append(VendorProfileInline(self.model, self.admin_site))
            elif obj.user_type == 'USER':
                inline_instances.append(UserProfileInline(self.model, self.admin_site))
        return inline_instances

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile,ModelAdmin)
admin.site.register(VendorProfile,ModelAdmin)