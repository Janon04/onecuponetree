from django.db import models


from django.utils.translation import gettext_lazy as _
from farmers.models import Farmer
from trees.models import Tree

class Contact(models.Model):
	name = models.CharField(_('name'), max_length=100)
	email = models.EmailField(_('email'))
	subject = models.CharField(_('subject'), max_length=200)
	message = models.TextField(_('message'))
	created_at = models.DateTimeField(_('created at'), auto_now_add=True)

	def __str__(self):
		return f"{self.name} - {self.subject}"

class Donation(models.Model):
    DONATION_TYPE_CHOICES = [
        ('general', _('General Initiative Support')),
        ('tree', _('Sponsor a Coffee Tree')),
        ('tour', _('Tourism Experience')),
    ]
    donor_name = models.CharField(_('Donor Name'), max_length=100, blank=True)
    donor_email = models.EmailField(_('Donor Email'), blank=True)
    amount = models.DecimalField(_('Amount (RWF)'), max_digits=10, decimal_places=2)
    donation_type = models.CharField(_('Donation Type'), max_length=10, choices=DONATION_TYPE_CHOICES)
    message = models.CharField(_('Message'), max_length=255, blank=True)
    tree = models.ForeignKey(Tree, on_delete=models.SET_NULL, null=True, blank=True, help_text=_('If sponsoring a tree'))
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True, blank=True, help_text=_('If supporting a farmer'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    payment_status = models.CharField(_('Payment Status'), max_length=20, default='pending')
    receipt_sent = models.BooleanField(_('Receipt Sent'), default=False)

    class Meta:
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name or 'Anonymous'} - {self.amount} RWF ({self.get_donation_type_display()})"
