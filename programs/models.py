from django.db import models
from ckeditor.fields import RichTextField

from django.utils.translation import gettext_lazy as _


class Program(models.Model):
	name = models.CharField(_('name'), max_length=200)
	description = RichTextField(_('description'), blank=True, null=True)
	image = models.ImageField(_('image'), upload_to='programs/images/', blank=True, null=True)
	video = models.FileField(_('video'), upload_to='programs/videos/', blank=True, null=True, help_text=_('Upload a short video (mp4, mov, webm, max 50MB)'))
	is_active = models.BooleanField(_('is active'), default=True)
	created_at = models.DateTimeField(_('created at'), auto_now_add=True)

	class Meta:
		verbose_name = _('Program')
		verbose_name_plural = _('Programs')
		ordering = ['name']

	def __str__(self):
		return self.name
