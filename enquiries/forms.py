from django import forms
from .models import Enquiry
import os

ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.webp']
MAX_FILE_SIZE_MB = 5

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            'customer_name', 'phone', 'email', 'service', 'product',
            'location', 'preferred_date', 'preferred_time', 'message',
            'attachment', 'source', 'calculation_details'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile / WhatsApp Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address (Optional)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Area Location'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Morning, 2 PM'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your requirements...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'source': forms.HiddenInput(),
            'calculation_details': forms.HiddenInput(),
            'service': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError("Please provide a valid phone number.")
        clean_digits = ''.join(filter(str.isdigit, phone))
        if len(clean_digits) < 8:
            raise forms.ValidationError("Please enter a valid phone number with at least 8 digits.")
        return phone

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            ext = os.path.splitext(attachment.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}")
            if attachment.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f"File size exceeds maximum limit of {MAX_FILE_SIZE_MB}MB.")
        return attachment
