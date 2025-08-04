from django import forms
from django.utils.translation import gettext_lazy as _
#from django.contrib.gis.forms import PointField
from .models import Tree
from apps.farmers.models import Farmer

class TreeTrackingForm(forms.Form):
    tree_id = forms.CharField(
        label=_('Tree ID'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your Tree ID'),
            'class': 'form-control-lg'
        }),
        help_text=_('You can find this on your certificate or reusable cup')
    )

class PlantTreeForm(forms.ModelForm):
    species = forms.ChoiceField(
        choices=Tree.TREE_SPECIES,
        label=_('Tree Species'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    """ location = PointField(
        label=_('Planting Location'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Latitude, Longitude')
        }) 
    
    ) """
    
    farmer = forms.ModelChoiceField(
        queryset=Farmer.objects.all(),
        required=False,
        label=_('Associated Farmer'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Tree
        fields = ['species', 'location', 'farmer', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        labels = {
            'photo': _('Tree Photo')
        }
        help_texts = {
            'photo': _('Upload a photo of the planted tree')
        }

class TreeUpdateForm(forms.ModelForm):
    co2_offset = forms.DecimalField(
        label=_('CO₂ Offset (kg)'),
        disabled=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    
    class Meta:
        model = Tree
        fields = ['species', 'location', 'farmer', 'photo', 'co2_offset', 'is_active']
        widgets = {
            'species': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude, Longitude'
            }),
            'farmer': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }

class TreeFilterForm(forms.Form):
    SPECIES_CHOICES = [('', _('All Species'))] + Tree.TREE_SPECIES
    
    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        required=False,
        label=_('Filter by Species'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        label=_('From Date'),
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        label=_('To Date'),
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    farmer = forms.ModelChoiceField(
        queryset=Farmer.objects.all(),
        required=False,
        label=_('Filter by Farmer'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )