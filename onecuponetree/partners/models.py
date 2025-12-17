from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

class Partner(models.Model):
    name = models.CharField(_('name'), max_length=200)
    logo = models.ImageField(_('logo'), upload_to='partners/logos/', blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    description = RichTextField(_('description'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
        ordering = ['name']

    def __str__(self):
        return self.name
