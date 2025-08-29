from django import forms
from .models import Farmer

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
