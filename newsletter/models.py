from django.db import models

from django.utils.translation import gettext_lazy as _

class Newsletter(models.Model):
    subject = models.CharField(_('subject'), max_length=255)
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    published = models.BooleanField(_('published'), default=False)
    sent_at = models.DateTimeField(_('sent at'), null=True, blank=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


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
