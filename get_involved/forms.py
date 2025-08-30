from django import forms
from .models import Volunteer, Partner
from django.utils.translation import gettext_lazy as _

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['skills', 'availability', 'interests']
        widgets = {
            'skills': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('List any relevant skills you have')
            }),
            'availability': forms.Select(attrs={
                'class': 'form-control'
            }),
            'interests': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('What areas are you most interested in?')
            }),
        }
        labels = {
            'skills': _('Your Skills'),
            'availability': _('Availability'),
            'interests': _('Areas of Interest'),
        }

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