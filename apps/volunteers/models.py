from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class BaristaTrainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    training_center = models.CharField(_('training center'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), null=True, blank=True)
    graduated = models.BooleanField(_('graduated'), default=False)
    internship_location = models.CharField(_('internship location'), max_length=100, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('Barista Trainee')
        verbose_name_plural = _('Barista Trainees')
    
    def __str__(self):
        return self.user.get_full_name()

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