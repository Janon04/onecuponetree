from django import forms
from django.utils.translation import gettext_lazy as _
from .models import InitiativeJoin, Partner
from django.core.exceptions import ValidationError

class InitiativeJoinForm(forms.ModelForm):
    class Meta:
        model = InitiativeJoin
        fields = [
            'join_as', 'full_name', 'gender', 'date_of_birth', 'nationality', 'national_id', 'profile_photo',
            'org_name', 'org_registration', 'org_type', 'org_contact_person', 'org_website', 'org_logo',
            'email', 'phone', 'country', 'province', 'district', 'sector', 'cell', 'village', 'how_heard',
            'purpose', 'skills', 'interests', 'availability', 'motivation', 'amount', 'preferred_location',
            'dedication_message', 'area_of_expertise', 'willing_to_mentor', 'resources_to_offer',
            'barista_experience', 'preferred_training', 'consent'
        ]
        widgets = {
            'join_as': forms.RadioSelect,
            'gender': forms.Select(choices=[('', '---'), ('male', _('Male')), ('female', _('Female')), ('other', _('Other'))]),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.RadioSelect(choices=[
                ('volunteer', _('Volunteer')),
                ('tree_sponsor', _('Tree Sponsor')),
                ('farmer_supporter', _('Farmer Supporter')),
                ('barista_academy', _('Barista Academy')),
                ('partner', _('Partner/Organization')),
                ('other', _('Other')),
            ]),
            'willing_to_mentor': forms.RadioSelect(choices=[(True, _('Yes')), (False, _('No'))]),
            'consent': forms.CheckboxInput,
        }

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id', '')
        if national_id:
            if not national_id.isdigit() or len(national_id) != 16:
                raise ValidationError(_('National ID must be exactly 16 digits.'))
        return national_id

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'partner_type', 'contact_person', 'email', 'phone', 'website']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Organization name')
            }),
            'contact_person': forms.TextInput(attrs={
                'placeholder': _('Full name')
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+250 123 456 789'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://yourwebsite.com'
            }),
        }
        labels = {
            'partner_type': _('Partner Type'),
            'contact_person': _('Contact Person'),
        }

class BaristaTrainingApplicationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        label=_('Full Name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('John Doe')
        })
    )
    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@email.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        label=_('Phone Number'),
        widget=forms.TextInput(attrs={
            'placeholder': '+250 123 456 789'
        })
    )
    education_level = forms.CharField(
        max_length=100,
        label=_('Education Level'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('High School, University, etc.')
        })
    )
    experience = forms.CharField(
        label=_('Previous Experience'),
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': _('Describe any relevant work experience')
        })
    )
    motivation = forms.CharField(
        label=_('Motivation Letter'),
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': _('Why do you want to join the Barista Training Program?')
        })
    )
