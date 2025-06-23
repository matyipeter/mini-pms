from django.contrib import admin
from .models import Lease, Payment

# Register your models here.
admin.site.register(Lease)
admin.site.register(Payment, list_display=['lease', 'amount', 'payment_date'], search_fields=['lease__tenant__user__username', 'lease__property__name'])
