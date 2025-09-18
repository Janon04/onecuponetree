from django import forms
from django.utils.translation import gettext_lazy as _
#from django.contrib.gis.forms import PointField
from apps.trees.models import Tree
from farmers.models import Farmer

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
    latitude = forms.DecimalField(
        label=_('Latitude'),
        required=False,
        initial=-0.0000,
        max_digits=9,
        decimal_places=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'value': '-0.0000', 'readonly': 'readonly'}),
        help_text=_('Latitude will be captured automatically (max 6 decimal places).')
    )
    longitude = forms.DecimalField(
        label=_('Longitude'),
        required=False,
        initial=00.000,
        max_digits=9,
        decimal_places=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001', 'value': '00.000', 'readonly': 'readonly'}),
        help_text=_('Longitude will be captured automatically (max 6 decimal places).')
    )
    species = forms.ChoiceField(
        choices=Tree.TREE_SPECIES,
        label=_('Tree Species'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_('Select the species of the tree planted.')
    )
    planted_date = forms.DateField(
        label=_('Planted Date'),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text=_('Enter the date the tree was planted.')
    )
    location = forms.ChoiceField(
        choices=[('', 'None')] + list(Tree.RWANDA_DISTRICTS),
        label=_('Location (District)'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_('Select the district where the tree was planted.')
    )
    farmer = forms.ModelChoiceField(
        queryset=Farmer.objects.all(),
        required=False,
        label=_('Associated Farmer'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text=_('Select the farmer associated with this tree (optional).')
    )
    planted_by = forms.CharField(
        label=_('Planted By'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name of person who planted')}),
        help_text=_('Enter the name of the person who planted the tree.')
    )

    class Meta:
        model = Tree
        fields = ['species', 'planted_date', 'location', 'latitude', 'longitude', 'farmer', 'planted_by', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        labels = {
            'photo': _('Tree Photo'),
        }
        help_texts = {
            'photo': _('Upload a photo of the planted tree'),
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


# --- New Form for Tree Planting Initiative ---
class TreePlantingInitiativeForm(forms.Form):
    latitude = forms.DecimalField(
        label=_('Latitude'),
        max_digits=9, decimal_places=6,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    longitude = forms.DecimalField(
        label=_('Longitude'),
        max_digits=9, decimal_places=6,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    TREE_TYPE_CHOICES = [
        ('mango', _('Mango')),
        ('coffee', _('Coffee')),
        ('eucalyptus', _('Eucalyptus')),
        ('avocado', _('Avocado')),
        ('other', _('Other')),
    ]
    CONTRIBUTION_TYPE_CHOICES = [
        ('self', _('I will provide and plant the trees myself 🌱')),
        ('donate', _('I will donate/provide trees for planting 🌳')),
        ('support', _('I will support others to plant trees (financial or logistical support) 💚')),
    ]

    tree_type = forms.ChoiceField(
        choices=TREE_TYPE_CHOICES,
        label=_('Tree Type'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        label=_('Quantity (Number of Trees)'),
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('How many trees?')})
    )
    country = forms.CharField(
        label=_('Country'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    province = forms.CharField(
        label=_('Province'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    district = forms.CharField(
        label=_('District'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sector = forms.CharField(
        label=_('Sector'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cell = forms.CharField(
        label=_('Cell'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    village = forms.CharField(
        label=_('Village'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    planting_date = forms.DateField(
        label=_('Planting Date'),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    contribution_type = forms.ChoiceField(
        choices=CONTRIBUTION_TYPE_CHOICES,
        label=_('Contribution Type'),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    full_name = forms.CharField(
        label=_('Your Full Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label=_('Email Address / Phone Number'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        label=_('Reason for Planting (Optional)'),
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': _('Why are you participating?')})
    )
    photo = forms.ImageField(
        label=_('Upload a Photo (Optional)'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
    )
    agreement = forms.BooleanField(
        label=_('I commit to ensuring the planted trees are cared for and maintained.'),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )