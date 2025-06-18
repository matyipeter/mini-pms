
from django import forms
from .models import MaintenanceRequest

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm',
                'placeholder': 'Title of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm',
                'placeholder': 'Describe the issue in detail...'
            }),
        }