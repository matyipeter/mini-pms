from django import forms
from .models import Lease
from users.models import TenantProfile

class LeaseForm(forms.ModelForm):
    tenant_email = forms.EmailField(
        label="Tenant Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Search by tenant email',
            'class': 'w-full px-4 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
        })
    )

    class Meta:
        model = Lease
        fields = ['property', 'start_date', 'end_date', 'rent_amount']

        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm'
            }),
            'rent_amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md shadow-sm'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("tenant_email")

        try:
            tenant = TenantProfile.objects.get(user__email=email)
            try:
                Lease.objects.get(tenant=tenant)
                self.add_error("tenant_email", "This tenant already has a lease.")
            except Lease.DoesNotExist:
                cleaned_data["tenant"] = tenant
        except TenantProfile.DoesNotExist:
            self.add_error("tenant_email", "No tenant with this email found.")
        
        return cleaned_data

    