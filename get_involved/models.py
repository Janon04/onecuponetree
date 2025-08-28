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

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(_('donation date'), auto_now_add=True)
    is_recurring = models.BooleanField(_('is recurring'), default=False)
    payment_method = models.CharField(_('payment method'), max_length=50)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
        ordering = ['-donation_date']
    
    def __str__(self):
        return f"Donation of {self.amount} by {self.donor}"