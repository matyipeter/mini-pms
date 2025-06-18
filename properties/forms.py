from django import forms
from .models import Property
from users.models import User


class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'city', 'state', 'zip_code', 'occupancy_status']

        widgets = {
            'address': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'state': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'zip_code': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'occupancy_status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

        
        