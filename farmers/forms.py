from django import forms
from .models import Farmer

class FarmSponsorshipForm(forms.Form):
    sponsor_name = forms.CharField(max_length=255, required=False, label="Your Name (optional)")
    sponsor_email = forms.EmailField(required=False, label="Email (for receipt, optional)")
    amount = forms.DecimalField(min_value=1, decimal_places=2, max_digits=10, label="Sponsorship Amount (USD)")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":2}), required=False, label="Message (optional)")


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: Only show 'barrier_other' if any barrier is checked
        if not (self.data.get('barrier_school_fees') or self.data.get('barrier_lack_materials') or self.data.get('barrier_distance') or self.data.get('barrier_early_marriage')):
            self.fields['barrier_other'].widget = forms.HiddenInput()
        # Example: Only show 'food_shortage_when' if food_shortage is True
        if not self.data.get('food_shortage'):
            self.fields['food_shortage_when'].widget = forms.HiddenInput()
        # Example: Only show 'chronic_illness_details' if has_chronic_illness is True
        if not self.data.get('has_chronic_illness'):
            self.fields['chronic_illness_details'].widget = forms.HiddenInput()
