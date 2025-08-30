from django.utils.translation import gettext_lazy as _
from django import forms
from .models import BaristaTraining, BaristaTrainingApplication

class BaristaTrainingForm(forms.ModelForm):
    class Meta:
        model = BaristaTraining
        fields = ['title', 'description', 'date', 'location', 'banner', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BaristaTrainingEventApplicationForm(forms.ModelForm):
    class Meta:
        model = BaristaTrainingApplication
        fields = ['name', 'email', 'phone', 'motivation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Why are you interested in this training?')}),
        }
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import VolunteerOpportunity, VolunteerApplication
from accounts.models import User

class VolunteerApplicationForm(forms.ModelForm):
    motivation = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': _('Why do you want to volunteer with us?')
        }),
        label=_('Motivation Letter')
    )
    
    skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': _('List any relevant skills or experience')
        }),
        label=_('Your Skills')
    )
    
    availability = forms.CharField(
        widget=forms.Select(choices=[
            ('weekdays', _('Weekdays')),
            ('weekends', _('Weekends')),
            ('both', _('Both weekdays and weekends')),
            ('flexible', _('Flexible'))
        ], attrs={'class': 'form-control'}),
        label=_('Availability')
    )

    class Meta:
        model = VolunteerApplication
        fields = ['motivation', 'skills', 'availability']
        labels = {
            'skills': _('Relevant Skills'),
            'availability': _('When are you available?')
        }

class VolunteerOpportunityForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': _('Detailed description of the opportunity')
        })
    )
    
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': _('Skills or qualifications needed')
        }),
        required=False
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )

    class Meta:
        model = VolunteerOpportunity
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 
                 'requirements', 'max_volunteers', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_volunteers': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'max_volunteers': _('Maximum number of volunteers'),
            'is_active': _('Is this opportunity currently available?')
        }



class VolunteerFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', _('All Statuses')),
        ('pending', _('Pending')),
        ('reviewed', _('Reviewed')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected'))
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Application Status')
    )
    
    opportunity = forms.ModelChoiceField(
        queryset=VolunteerOpportunity.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Filter by Opportunity')
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label=_('From Date')
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label=_('To Date')
    )