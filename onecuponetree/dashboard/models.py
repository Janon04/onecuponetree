from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class ImpactStat(models.Model):
    stat_name = models.CharField(_('stat name'), max_length=100)
    stat_value = models.IntegerField(_('stat value'))
    stat_icon = models.CharField(_('stat icon'), max_length=50, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Impact Stat')
        verbose_name_plural = _('Impact Stats')
    
    def __str__(self):
        return self.stat_name

class Testimonial(models.Model):
    author = models.CharField(_('author'), max_length=100)
    role = models.CharField(_('role'), max_length=100, blank=True)
    content = RichTextField(_('content'))
    photo = models.ImageField(_('photo'), upload_to='testimonials/', blank=True, null=True)
    video = models.FileField(_('video'), upload_to='testimonials/videos/', blank=True, null=True, help_text=_('Upload a short video testimonial (mp4, mov, webm, max 50MB)'))
    is_featured = models.BooleanField(_('is featured'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.author}"