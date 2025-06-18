from django.db import models
from django.contrib.auth.models import AbstractUser
from properties.models import Property

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [('owner', 'Owner'), ('tenant', 'Tenant')]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

    def is_owner(self):
        return self.role == 'owner'

    def is_tenant(self):
        return self.role == 'tenant'


class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def add_property(self, **data):
        property = Property.objects.create(
            owner=self,
            address = data['address'],
            typ = data['typ'],
            available = data['available']
        )
        
        property.save()
        self.save()

    def remove_property(self, property_id):
        property = self.get_property(property_id)
        property.delete()
        property.save()
        self.save()

    def get_property(self, property_id):
        return self.properties.get(id=property_id)

    def update_property(self, property_id, **kwargs):
        property = self.get_property(property_id)
        for key, value in kwargs.items():
            setattr(property, key, value)
        property.save()

    def get_properties(self):
        return self.properties.all()

    def __str__(self):
        return self.user.username



class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def pay_rent(self, amount):
        pass

    def view_lease(self):
        return self.lease

    def __str__(self):
        return self.user.username