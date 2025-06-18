from django.db import models
# Create your models here.

class Property(models.Model):
    
    owner = models.ForeignKey('users.OwnerProfile', on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    typ = models.CharField(
        choices=[
            ('house', 'House'),
            ('apartment', 'Apartment'),
            ('other', 'Other'),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    occupancy_status = models.CharField(
        choices=[
            ('available', 'Available'),
            ('occupied', 'Occupied'),
            ('maintenance', 'Maintenance'),
        ]
    )

    # leases[]
    # maintanacerequests[]

    #####

    def is_available(self):
        return self.occupancy_status == 'available'

    def set_status(self, status):
        self.occupancy_status = status
        self.save()

    def get_current_lease(self):
        if self.leases.exists():
            return self.leases.first()
        return None
    
    def get_lease_history(self):
        return self.leases.all()

    def get_lease(self, lease_id):
        return self.leases.get(id=lease_id)

    def add_maintenance_request(self, request):
        self.maintanacerequests.add(request)
        self.save()
    
    def get_maintenance_history(self):
        return self.maintanacerequests.all()

    def __str__(self):
        return f'{self.address} - {self.typ}'