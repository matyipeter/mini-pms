from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm
from properties.models import Property
from lease.models import Lease
from users.models import TenantProfile

class MaintenanceRequestCreateView(CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "maintenance/request_form.html"

    def form_valid(self, form):
        tenant = get_object_or_404(TenantProfile, user=self.request.user)
        lease = Lease.objects.filter(tenant=tenant).first()
        print(lease.created_at)

        form.instance.tenant = tenant
        form.instance.property = lease.property
        if form.instance.property is None:
            print("Maintenance request cannot be created without an active lease.")
        form.instance.status = 'pending'
        return super().form_valid(form)

    def get_success_url(self):
        
        return reverse_lazy("properties:property_detail", kwargs={"pk": self.object.property.pk})

    
        
