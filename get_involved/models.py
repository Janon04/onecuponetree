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

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.TextField(_('skills'), blank=True)
    availability = models.CharField(_('availability'), max_length=100, blank=True)
    interests = models.TextField(_('interests'), blank=True)
    joined_date = models.DateField(_('joined date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Volunteer')
        verbose_name_plural = _('Volunteers')
    
    def __str__(self):
        if self.user:
            return self.user.get_full_name()
        return f"Volunteer #{self.pk}"

