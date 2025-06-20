from django.contrib import admin
from .models import Report

# Register your models here.

admin.site.register(Report, list_display=['owner', 'created_at', 'number_of_properties', 'number_of_tenants', 'monthly_income', 'monthly_expenses', 'available_properties', 'occupied_properties'], search_fields=['owner__user__username'])
