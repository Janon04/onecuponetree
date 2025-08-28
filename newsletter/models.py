from django.db import models
from django.utils.translation import gettext_lazy as _

class NewsletterSubscriber(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    subscribed_at = models.DateTimeField(_('subscribed at'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('Newsletter Subscriber')
        verbose_name_plural = _('Newsletter Subscribers')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
