from django.db import models

from django.utils.translation import gettext_lazy as _

class Program(models.Model):
	name = models.CharField(_('name'), max_length=200)
	description = models.TextField(_('description'), blank=True, null=True)
	is_active = models.BooleanField(_('is active'), default=True)
	created_at = models.DateTimeField(_('created at'), auto_now_add=True)

	class Meta:
		verbose_name = _('Program')
		verbose_name_plural = _('Programs')
		ordering = ['name']

	def __str__(self):
		return self.name
