from django.contrib import admin
from .models import User, OwnerProfile, TenantProfile

# Register your models here.

admin.site.register(User)
admin.site.register(OwnerProfile)
admin.site.register(TenantProfile)

