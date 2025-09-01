
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class PublicationDownloadRequest(models.Model):
	publication = models.ForeignKey('ResearchPublication', on_delete=models.CASCADE, related_name='download_requests')
	name = models.CharField(max_length=100)
	email = models.EmailField()
	reason = models.TextField(blank=True)
	approved = models.BooleanField(default=False)
	requested_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name = 'Publication Download Request'
		verbose_name_plural = 'Publication Download Requests'
		ordering = ['-requested_at']

	def __str__(self):
		return f"{self.name} - {self.publication.title} ({'Approved' if self.approved else 'Pending'})"


from django.db import models
from django.utils.translation import gettext_lazy as _

class ResearchCategory(models.Model):
	name = models.CharField(_('Category Name'), max_length=100, unique=True)
	from ckeditor.fields import RichTextField
	description = RichTextField(_('Description'), blank=True)
	is_active = models.BooleanField(_('Active'), default=True)

	class Meta:
		verbose_name = _('Research Category')
		verbose_name_plural = _('Research Categories')
		ordering = ['name']

	def __str__(self):
		return self.name

class ResearchPublication(models.Model):
	category = models.ForeignKey(ResearchCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='publications', verbose_name=_('Category'))
	title = models.CharField(_('Title'), max_length=200)
	summary = RichTextField(_('Summary'), blank=True)
	author = models.CharField(_('Author(s)'), max_length=100, blank=True)
	publication_date = models.DateField(_('Publication Date'), blank=True, null=True)
	document = models.FileField(_('Document (PDF, DOC, etc.)'), upload_to='research_documents/', blank=True, null=True)
	image = models.ImageField(_('Cover Image'), upload_to='research_images/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(_('Active/Visible'), default=True)

	class Meta:
		verbose_name = _('Research Publication')
		verbose_name_plural = _('Research Publications')
		ordering = ['-publication_date', '-created_at']

	def __str__(self):
		return self.title
