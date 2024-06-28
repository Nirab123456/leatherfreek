# forms.py
from django import forms
from .models import contact_us

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = ['contact_name', 'phone_number', 'contact_email', 'contact_message']
