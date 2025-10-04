from django.db import models
from django.utils.translation import gettext_lazy as _

class GalleryImage(models.Model):
    pinned = models.BooleanField(_('pinned'), default=False, help_text=_('Pin this item to keep it at the top of the gallery'))
    title = models.CharField(_('title'), max_length=200)
    image = models.ImageField(_('image'), upload_to='gallery/', null=True, blank=True)
    video = models.FileField(_('video'), upload_to='gallery/videos/', null=True, blank=True, help_text=_('Upload a short video (mp4, mov, webm, max 50MB)'))
    description = models.TextField(_('description'), blank=True, null=True)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Gallery Image')
        verbose_name_plural = _('Gallery Images')
        ordering = ['-pinned', '-uploaded_at']

    def __str__(self):
        return self.title
