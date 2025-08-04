from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSetting(models.Model):
    site_name = models.CharField(_('site name'), max_length=100, default='One Cup One Tree')
    site_description = models.TextField(_('site description'), blank=True)
    logo = models.ImageField(_('logo'), upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(_('favicon'), upload_to='site/', blank=True, null=True)
    contact_email = models.EmailField(_('contact email'), blank=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, blank=True)
    address = models.TextField(_('address'), blank=True)
    facebook_url = models.URLField(_('facebook url'), blank=True)
    twitter_url = models.URLField(_('twitter url'), blank=True)
    instagram_url = models.URLField(_('instagram url'), blank=True)
    youtube_url = models.URLField(_('youtube url'), blank=True)
    
    class Meta:
        app_label = 'core'
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return self.site_name
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj