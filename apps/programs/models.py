from django.db import models
from django.utils.translation import gettext_lazy as _

class Program(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
    icon = models.CharField(_('icon'), max_length=50, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')
    
    def __str__(self):
        return self.name

class BaristaTraining(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name='barista_training')
    locations = models.TextField(_('locations'))
    duration = models.CharField(_('duration'), max_length=50)
    curriculum = models.TextField(_('curriculum'))
    scholarship_available = models.BooleanField(_('scholarship available'), default=True)
    
    class Meta:
        verbose_name = _('Barista Training')
        verbose_name_plural = _('Barista Trainings')
    
    def __str__(self):
        return f"Barista Training - {self.program.name}"

class FarmerSupport(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name='farmer_support')
    services = models.TextField(_('services'))
    distribution_centers = models.TextField(_('distribution centers'))
    training_topics = models.TextField(_('training topics'))
    
    class Meta:
        verbose_name = _('Farmer Support')
        verbose_name_plural = _('Farmer Supports')
    
    def __str__(self):
        return f"Farmer Support - {self.program.name}"

class ReusableCupCampaign(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name='reusable_cup_campaign')
    cup_types = models.TextField(_('cup types'))
    incentives = models.TextField(_('incentives'))
    distribution_points = models.TextField(_('distribution points'))
    
    class Meta:
        verbose_name = _('Reusable Cup Campaign')
        verbose_name_plural = _('Reusable Cup Campaigns')
    
    def __str__(self):
        return f"Reusable Cup Campaign - {self.program.name}"