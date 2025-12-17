import datetime
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
    from .models import Motivation, ExpectedSkill, Skill
    motivation = forms.ModelMultipleChoiceField(
        queryset=Motivation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Why do you want to attend this training?',
    )
    expected_skills = forms.ModelMultipleChoiceField(
        queryset=ExpectedSkill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='What skills or knowledge do you expect to gain?',
    )
    skills_experience = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Relevant Skills or Experience',
    )
    # ModelMultipleChoiceField handles saving ManyToMany relationships automatically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs['readonly'] = True
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number', '')
        if not id_number.isdigit() or len(id_number) > 16:
            raise forms.ValidationError('National ID must be up to 16 digits.')
        return id_number

    def clean(self):
        cleaned_data = super().clean()
        id_number = cleaned_data.get('id_number', '')
        # Auto-calculate age from ID if possible (Rwanda NID: 2nd-5th digits = YYYY, 6-7th = MM, 8-9th = DD)
        if id_number and len(id_number) == 16 and id_number.isdigit():
            year = int(id_number[1:5])
            month = int(id_number[5:7])
            day = int(id_number[7:9])
            try:
                birth_date = datetime.date(year, month, day)
                today = datetime.date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                cleaned_data['age'] = age
                cleaned_data['date_of_birth'] = birth_date
            except Exception:
                pass
        return cleaned_data
    class Meta:
        model = BaristaTrainingApplication
        fields = [
            # 1. Personal Information
            'full_name', 'date_of_birth', 'age', 'gender', 'nationality', 'id_number',
            # 2. Contact Information
            'phone', 'email', 'country', 'province', 'district', 'sector', 'cell', 'village',
            # 3. Educational & Professional Background
            'education_level', 'occupation', 'skills_experience',
            # 4. Training-Specific Information
            'motivation', 'expected_skills', 'attended_similar', 'attended_similar_details', 'preferred_location', 'availability',
            # 5. Additional Information
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone', 'special_needs', 'languages_spoken',
            # 6. Declaration & Consent
            'confirm_information', 'agree_participation', 'signature_name', 'signature_date',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'cell': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.Select(attrs={'class': 'form-select'}),
            'attended_similar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attended_similar_details': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_location': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'special_needs': forms.TextInput(attrs={'class': 'form-control'}),
            'languages_spoken': forms.TextInput(attrs={'class': 'form-control'}),
            'confirm_information': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'agree_participation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'signature_name': forms.TextInput(attrs={'class': 'form-control'}),
            'signature_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    special_needs = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Special Needs (Optional)'
    )
    languages_spoken = forms.MultipleChoiceField(
        required=True,
        choices=[
            ('english', 'English'),
            ('french', 'French'),
            ('kinyarwanda', 'Kinyarwanda'),
            ('kiswahili', 'Kiswahili'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Languages Spoken'
    )
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import VolunteerOpportunity, VolunteerApplication
from accounts.models import User

class VolunteerApplicationForm(forms.ModelForm):
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number', '')
        if len(id_number) > 16:
            raise forms.ValidationError('National ID should not exceed 16 digits.')
        if not id_number.isdigit():
            raise forms.ValidationError('National ID should contain only digits.')
        return id_number
    # 1. Personal Information
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Full Name'
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date of Birth'
    )
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender'
    )
    id_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'maxlength': '16',
            'inputmode': 'numeric',
            'pattern': '[0-9]{1,16}',
            'placeholder': '16 digits max'
        }),
        label='National ID/Passport No.'
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Phone Number'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email Address'
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Country'
    )
    province = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Province/District'
    )
    sector_cell_village = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Sector/Cell/Village'
    )

    # 2. Motivation Letter
    motivation = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Why do you want to volunteer with us?'}),
        label='Motivation Letter'
    )

    # 3. Relevant Skills & Experience
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'List any relevant skills or experience'}),
        label='Relevant Skills & Experience'
    )

    # 4. Availability
    availability_weekdays = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify times'}),
        label='Weekdays (specify times)'
    )
    availability_weekends = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Weekends'
    )
    availability_full_time = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Full-time'
    )
    availability_part_time = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Part-time'
    )
    availability_specific_dates = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specific dates'}),
        label='Specific dates'
    )

    # 5. Areas of Interest
    interest_community_outreach = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Community Outreach')
    interest_event_support = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Event Support')
    interest_training_mentorship = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Training & Mentorship')
    interest_environmental = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Environmental Activities (tree planting, farming, etc.)')
    interest_fundraising = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Fundraising & Campaigns')
    interest_admin_support = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Administrative Support')
    interest_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other'}), label='Other')

    # 6. Emergency Contact
    emergency_contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Emergency Contact Name')
    emergency_contact_relationship = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Relationship')
    emergency_contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Emergency Contact Phone')

    # 7. References (Optional)

    # 8. Declaration & Signature
    declaration = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='I confirm that the above information is true and complete.')
    signature_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Signature (Full Name)')
    signature_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Date')

    class Meta:
        model = VolunteerApplication
        fields = [
            'full_name', 'date_of_birth', 'gender', 'id_number', 'phone', 'email', 'country', 'province', 'sector_cell_village',
            'motivation', 'skills',
            'availability_weekdays', 'availability_weekends', 'availability_full_time', 'availability_part_time', 'availability_specific_dates',
            'interest_community_outreach', 'interest_event_support', 'interest_training_mentorship', 'interest_environmental', 'interest_fundraising', 'interest_admin_support', 'interest_other',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'declaration', 'signature_name', 'signature_date',
        ]

class VolunteerOpportunityForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Detailed description of the opportunity'
        })
    )
    
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Skills or qualifications needed'
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

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Image (jpg, png, webp, max 5MB)'
    )
    video = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Video (mp4, mov, webm, max 50MB)'
    )

    class Meta:
        model = VolunteerOpportunity
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 
                 'requirements', 'image', 'video', 'max_volunteers', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_volunteers': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'max_volunteers': 'Maximum number of volunteers',
            'is_active': 'Is this opportunity currently available?'
        }



class VolunteerFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Application Status'
    )
    
    opportunity = forms.ModelChoiceField(
        queryset=VolunteerOpportunity.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Opportunity'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )