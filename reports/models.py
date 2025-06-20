from django.db import models

# Create your models here.

class Report(models.Model):
    
    owner = models.ForeignKey('users.OwnerProfile', on_delete=models.CASCADE, related_name='reports')
    number_of_properties = models.IntegerField(default=0, blank=True, null=True)
    number_of_tenants = models.IntegerField(default=0, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    available_properties = models.IntegerField(default=0, blank=True, null=True)
    occupied_properties = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Report for {self.owner.user.username} - {self.created_at.strftime("%Y-%m-%d")}'
