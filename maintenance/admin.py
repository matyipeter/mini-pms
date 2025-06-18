from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MaintenanceRequest, list_display=['title', 'tenant', 'property', 'status', 'created_at'], search_fields=['title', 'tenant__user__username', 'property__name'])
