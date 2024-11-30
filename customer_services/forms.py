from django import forms
from .models import ServiceRequest, Customer


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['type', 'description', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'contact_number']
