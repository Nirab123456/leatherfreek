# forms.py
from django import forms
from .models import contact_us , User_Record

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = ['contact_name', 'phone_number', 'contact_email', 'contact_message']



class UserRecordForm(forms.ModelForm):
    class Meta:
        model = User_Record
        fields = ['first_name', 'last_name', 'user_email', 'user_phone' ,'country', 'city','zip_code','address']
        
