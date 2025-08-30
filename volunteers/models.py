from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class BaristaTraining(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    date = models.DateField(_('training date'))
    location = models.CharField(_('location'), max_length=100)
    banner = models.ImageField(_('banner or pullup'), upload_to='barista_training_banners/', blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Barista Training')
        verbose_name_plural = _('Barista Trainings')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class BaristaTrainingApplication(models.Model):
    training = models.ForeignKey(BaristaTraining, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=30, blank=True)
    motivation = models.TextField(_('motivation'), blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Barista Training Application')
        verbose_name_plural = _('Barista Training Applications')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.name} - {self.training.title}"
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class VolunteerOpportunity(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    location = models.CharField(_('location'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    skills_required = models.TextField(_('skills required'), blank=True)
    max_volunteers = models.PositiveIntegerField(_('maximum volunteers'), default=1)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Volunteer Opportunity')
        verbose_name_plural = _('Volunteer Opportunities')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title

class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_date = models.DateTimeField(_('application date'), auto_now_add=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('Volunteer Application')
        verbose_name_plural = _('Volunteer Applications')
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.user} - {self.opportunity}"