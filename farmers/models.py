from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.gis.db import models as gis_models

from accounts.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(_('location'), max_length=255, blank=True)
    farm_size = models.DecimalField(_('farm size (hectares)'), max_digits=10, decimal_places=2)
    joined_date = models.DateField(_('joined date'))
    bio = models.TextField(_('bio'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='farmers/', null=True, blank=True)
    is_featured = models.BooleanField(_('is featured'), default=False)

    class Meta:
        verbose_name = _('Farmer')
        verbose_name_plural = _('Farmers')

    def __str__(self):
        return self.user.get_full_name()


# FarmerSupportActivity should be a top-level model, not nested inside Farmer
class FarmerSupportActivity(models.Model):
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, related_name='support_activities')
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True, null=True)
    date = models.DateField(_('date'))
    support_type = models.CharField(_('support type'), max_length=100)
    is_successful = models.BooleanField(_('is successful'), default=True)

    class Meta:
        verbose_name = _('Farmer Support Activity')
        verbose_name_plural = _('Farmer Support Activities')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.farmer.user.get_full_name()})"

class FarmerStory(models.Model):
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    photo = models.ImageField(_('photo'), upload_to='farmer_stories/', blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    is_published = models.BooleanField(_('is published'), default=True)
    
    class Meta:
        verbose_name = _('Farmer Story')
        verbose_name_plural = _('Farmer Stories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.farmer}"