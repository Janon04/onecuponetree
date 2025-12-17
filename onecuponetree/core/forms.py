from django import forms
from .models import TeamMember

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'title', 'photo', 'bio', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin', 'order']
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
            'donor_name', 'donor_email', 'phone', 'country', 'province_district',
            'donation_frequency', 'amount', 'currency', 'donation_type',
            'transaction_reference', 'purpose', 'message', 'tree', 'farmer',
            'public_acknowledgement', 'communication_opt_in', 'declaration',
            'donor_signature', 'signature_date'
        ]
        widgets = {
            'donation_type': forms.RadioSelect,
            'donation_frequency': forms.RadioSelect,
            'purpose': forms.RadioSelect,
            'public_acknowledgement': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No (Anonymous Donation)')]),
            'communication_opt_in': forms.RadioSelect(choices=[(True, 'I would like to receive updates'), (False, 'No updates, donation only')]),
            'declaration': forms.CheckboxInput,
            'signature_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide tree/farmer fields unless relevant
        if self.data.get('donation_type') != 'tree':
            self.fields['tree'].widget = forms.HiddenInput()
        if self.data.get('donation_type') != 'tour':
            self.fields['farmer'].widget = forms.HiddenInput()
        self.fields['declaration'].label = 'I confirm that the information provided is correct and this donation is made willingly.'
        self.fields['purpose'].required = False
