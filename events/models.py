from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
	"""Model representing an event."""
	STATUS_CHOICES = [
		('upcoming', _('Upcoming')),
		('ongoing', _('Ongoing')),
		('completed', _('Completed')),
		('cancelled', _('Cancelled')),
	]

	title = models.CharField(max_length=200, help_text=_('Event title'))
	description = models.TextField(help_text=_('Event description'))
	start_date = models.DateTimeField(help_text=_('Event start date and time'))
	end_date = models.DateTimeField(help_text=_('Event end date and time'))
	location = models.CharField(max_length=255, help_text=_('Event location'))
	organizer = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='organized_events',
		help_text=_('Event organizer')
	)
	status = models.CharField(
		max_length=20,
		choices=STATUS_CHOICES,
		default='upcoming',
		help_text=_('Event status')
	)
	image = models.ImageField(
		upload_to='events/',
		null=True,
		blank=True,
		help_text=_('Event image or banner')
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Translation registration will be handled in translation.py

	class Meta:
		verbose_name = _('Event')
		verbose_name_plural = _('Events')
		ordering = ['-start_date']

	def __str__(self):
		return f"{self.title} ({self.get_status_display()})"
