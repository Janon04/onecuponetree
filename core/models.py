
from django.db import models


from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
	name = models.CharField(_('name'), max_length=100)
	email = models.EmailField(_('email'))
	subject = models.CharField(_('subject'), max_length=200)
	message = models.TextField(_('message'))
	created_at = models.DateTimeField(_('created at'), auto_now_add=True)

	def __str__(self):
		return f"{self.name} - {self.subject}"
