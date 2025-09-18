from django.db import models


from django.utils.translation import gettext_lazy as _
from farmers.models import Farmer
from apps.trees.models import Tree

class Contact(models.Model):
	name = models.CharField(_('name'), max_length=100)
	email = models.EmailField(_('email'))
	subject = models.CharField(_('subject'), max_length=200)
	message = models.TextField(_('message'))
	created_at = models.DateTimeField(_('created at'), auto_now_add=True)

	def __str__(self):
		return f"{self.name} - {self.subject}"

class Donation(models.Model):
    # New fields for professional donation form
    phone = models.CharField(_('Phone Number'), max_length=30, blank=True)
    country = models.CharField(_('Country'), max_length=100, blank=True)
    province_district = models.CharField(_('Province / District'), max_length=100, blank=True)
    DONATION_FREQ_CHOICES = [
        ('one_time', _('One-time Donation')),
        ('recurring', _('Monthly / Recurring Donation')),
    ]
    donation_frequency = models.CharField(_('Donation Frequency'), max_length=20, choices=DONATION_FREQ_CHOICES, default='one_time')
    CURRENCY_CHOICES = [
        ('RWF', 'RWF'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('KES', 'KES'),
        ('UGX', 'UGX'),
        ('Other', _('Other')),
    ]
    currency = models.CharField(_('Currency'), max_length=10, choices=CURRENCY_CHOICES, default='RWF')
    MODE_CHOICES = [
        ('mobile_money', _('Mobile Money (MTN / Airtel)')),
        ('bank_transfer', _('Bank Transfer')),
        ('card', _('Credit/Debit Card')),
        ('cash', _('Cash')),
        ('other', _('Other')),
    ]
    donation_mode = models.CharField(_('Mode of Donation'), max_length=20, choices=MODE_CHOICES, default='mobile_money')
    transaction_reference = models.CharField(_('Transaction Reference Number'), max_length=100, blank=True)
    PURPOSE_CHOICES = [
        ('training', _('Training Programs')),
        ('community', _('Community Projects')),
        ('equipment', _('Equipment / Materials')),
        ('general', _('General Support (where most needed)')),
    ]
    purpose = models.CharField(_('Purpose of Donation'), max_length=20, choices=PURPOSE_CHOICES, blank=True)
    public_acknowledgement = models.BooleanField(_('Publicly acknowledge as donor?'), default=True)
    communication_opt_in = models.BooleanField(_('Receive updates about the initiative?'), default=True)
    declaration = models.BooleanField(_('I confirm this donation is made willingly.'), default=False)
    donor_signature = models.CharField(_('Full Name of Donor (as signature)'), max_length=100, blank=True)
    signature_date = models.DateField(_('Date of signature'), null=True, blank=True)
    DONATION_TYPE_CHOICES = [
        ('general', _('General Initiative Support')),
        ('tree', _('Sponsor a Coffee Tree')),
        ('tour', _('Tourism Experience')),
    ]
    donor_name = models.CharField(_('Donor Name'), max_length=100, blank=True)
    donor_email = models.EmailField(_('Donor Email'), blank=True)
    amount = models.FloatField(_('Amount (RWF)'))
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
