from django.db import models

# Create your models here.

class MaintenanceRequest(models.Model):
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    tenant = models.ForeignKey('users.TenantProfile', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    