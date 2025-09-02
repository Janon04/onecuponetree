from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

class Event(models.Model):
	"""Model representing an event."""
	STATUS_CHOICES = [
		('upcoming', 'Upcoming'),
		('ongoing', 'Ongoing'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	]

	title = models.CharField(max_length=200, help_text='Event title')
	from ckeditor.fields import RichTextField
	description = RichTextField(help_text='Event description')
	start_date = models.DateTimeField(help_text='Event start date and time')
	end_date = models.DateTimeField(help_text='Event end date and time')
	location = models.CharField(max_length=255, help_text='Event location')
	organizer = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='organized_events',
	help_text='Event organizer'
	)
	status = models.CharField(
		max_length=20,
		choices=STATUS_CHOICES,
		default='upcoming',
	help_text='Event status'
	)
	image = models.ImageField(
		upload_to='events/',
		null=True,
		blank=True,
	help_text='Event image or banner'
	)
	video = models.FileField(
		upload_to='events/videos/',
		null=True,
		blank=True,
	help_text='Upload a short video (mp4, mov, webm, max 50MB)'
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		verbose_name = 'Event'
		verbose_name_plural = 'Events'
		ordering = ['-start_date']

	def __str__(self):
		return f"{self.title} ({self.get_status_display()})"
