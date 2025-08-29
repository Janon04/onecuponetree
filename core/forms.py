from django import forms
from .models import Contact, Donation

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'donor_name', 'donor_email', 'amount', 'donation_type', 'message', 'tree', 'farmer'
        ]
        widgets = {
            'donation_type': forms.RadioSelect,
            'message': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide tree/farmer fields unless relevant
        if self.data.get('donation_type') != 'tree':
            self.fields['tree'].widget = forms.HiddenInput()
        if self.data.get('donation_type') != 'tour':
            self.fields['farmer'].widget = forms.HiddenInput()
