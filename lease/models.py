from django.db import models
from datetime import datetime

# Create your models here.

class Lease(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='lease')
    tenant = models.OneToOneField('users.TenantProfile', on_delete=models.CASCADE, related_name='lease')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_active(self):
        self.is_active = True
        self.property.occupancy_status = 'Occupied'
        self.property.save()
    
    def calculate_remaining_days(self):
        return (self.end_date - datetime.date.today()).days

    def renew(self, new_date):
        self.end_date = new_date
        self.save()

    def terminate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.property} - {self.tenant}'
    
    