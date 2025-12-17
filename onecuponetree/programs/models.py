from django.db import models
from ckeditor.fields import RichTextField



class Program(models.Model):
	name = models.CharField('Name', max_length=200)
	description = RichTextField('Description', blank=True, null=True)
	image = models.ImageField('Image', upload_to='programs/images/', blank=True, null=True)
	video = models.FileField('Video', upload_to='programs/videos/', blank=True, null=True, help_text='Upload a short video (mp4, mov, webm, max 50MB)')
	is_active = models.BooleanField('Is active', default=True)
	created_at = models.DateTimeField('Created at', auto_now_add=True)

	class Meta:
		verbose_name = 'Program'
		verbose_name_plural = 'Programs'
		ordering = ['name']

	def __str__(self):
		return self.name
