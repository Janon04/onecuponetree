from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

class InitiativeJoin(models.Model):
    JOIN_AS_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization/Company'),
    ]
    join_as = models.CharField(_('Joining As'), max_length=20, choices=JOIN_AS_CHOICES)

    # Common fields
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone Number'), max_length=30, blank=True)
    country = models.CharField(_('Country'), max_length=100, blank=True)
    province = models.CharField(_('Province/State'), max_length=100, blank=True)
    district = models.CharField(_('District'), max_length=100, blank=True)
    sector = models.CharField(_('Sector'), max_length=100, blank=True)
    cell = models.CharField(_('Cell'), max_length=100, blank=True)
    village = models.CharField(_('Village'), max_length=100, blank=True)
    how_heard = models.CharField(_('How did you hear about us?'), max_length=100, blank=True)

    # Individual fields
    full_name = models.CharField(_('Full Name'), max_length=100, blank=True)
    gender = models.CharField(_('Gender'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    nationality = models.CharField(_('Nationality'), max_length=50, blank=True)
    national_id = models.CharField(_('National ID/Passport Number'), max_length=16, blank=True)
    occupation = models.CharField(_('Occupation/Profession'), max_length=100, blank=True)
    profile_photo = models.ImageField(_('Profile Photo'), upload_to='volunteers/photos/', blank=True, null=True)

    # Organization fields
    org_name = models.CharField(_('Organization/Company Name'), max_length=200, blank=True)
    org_registration = models.CharField(_('Registration Number'), max_length=50, blank=True)
    org_type = models.CharField(_('Organization Type'), max_length=50, blank=True)
    org_contact_person = models.CharField(_('Contact Person Name'), max_length=100, blank=True)
    org_website = models.URLField(_('Website'), blank=True)
    org_logo = models.ImageField(_('Logo'), upload_to='organizations/logos/', blank=True, null=True)

    # Purpose/Role
    purpose = models.CharField(_('Purpose/Role'), max_length=50)
    # Details for each purpose
    skills = RichTextField(_('Skills'), blank=True)
    interests = RichTextField(_('Areas of Interest'), blank=True)
    availability = models.CharField(_('Availability'), max_length=100, blank=True)
    motivation = RichTextField(_('Motivation/Why do you want to join?'), blank=True)
    amount = models.DecimalField(_('Sponsorship Amount'), max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_location = models.CharField(_('Preferred Location'), max_length=100, blank=True)
    dedication_message = models.CharField(_('Dedication Message'), max_length=255, blank=True)
    area_of_expertise = models.CharField(_('Area of Expertise'), max_length=100, blank=True)
    willing_to_mentor = models.BooleanField(_('Willing to Mentor'), default=False)
    resources_to_offer = RichTextField(_('Resources to Offer'), blank=True)
    barista_experience = models.TextField(_('Barista Experience'), blank=True)
    preferred_training = models.CharField(_('Preferred Training'), max_length=100, blank=True)

    consent = models.BooleanField(_('I agree to the terms and privacy policy'), default=False)
    submitted_at = models.DateTimeField(_('Submitted At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Initiative Join')
        verbose_name_plural = _('Initiative Joins')
        ordering = ['-submitted_at']

    def __str__(self):
        if self.join_as == 'organization':
            return f"{self.org_name} (Organization)"
        return f"{self.full_name} (Individual)"
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class Partner(models.Model):
    PARTNER_TYPES = (
        ('corporate', 'Corporate'),
        ('ngo', 'NGO'),
        ('government', 'Government'),
        ('individual', 'Individual'),
    )
    
    name = models.CharField(_('name'), max_length=200)
    partner_type = models.CharField(_('partner type'), max_length=20, choices=PARTNER_TYPES)
    contact_person = models.CharField(_('contact person'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=20)
    website = models.URLField(_('website'), blank=True)
    logo = models.ImageField(_('logo'), upload_to='partners/', blank=True, null=True)
    joined_date = models.DateField(_('joined date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
    
    def __str__(self):
        return self.name


