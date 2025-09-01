
from django.db import models
from django.utils.translation import gettext_lazy as _

class TreePlantingSubmission(models.Model):
    TREE_TYPE_CHOICES = [
        ('mango', _('Mango')),
        ('coffee', _('Coffee')),
        ('eucalyptus', _('Eucalyptus')),
        ('avocado', _('Avocado')),
        ('other', _('Other')),
    ]
    CONTRIBUTION_TYPE_CHOICES = [
        ('self', _('I will provide and plant the trees myself 🌱')),
        ('donate', _('I will donate/provide trees for planting 🌳')),
        ('support', _('I will support others to plant trees (financial or logistical support) 💚')),
    ]

    tree_type = models.CharField(_('Tree Type'), max_length=32, choices=TREE_TYPE_CHOICES)
    quantity = models.PositiveIntegerField(_('Quantity (Number of Trees)'))
    country = models.CharField(_('Country'), max_length=64)
    province = models.CharField(_('Province'), max_length=64)
    district = models.CharField(_('District'), max_length=64)
    sector = models.CharField(_('Sector'), max_length=64)
    cell = models.CharField(_('Cell'), max_length=64)
    village = models.CharField(_('Village'), max_length=64)
    latitude = models.DecimalField(_('Latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    planting_date = models.DateField(_('Planting Date'))
    contribution_type = models.CharField(_('Contribution Type'), max_length=32, choices=CONTRIBUTION_TYPE_CHOICES)
    full_name = models.CharField(_('Your Full Name'), max_length=128)
    contact = models.CharField(_('Email Address / Phone Number'), max_length=128)
    reason = models.TextField(_('Reason for Planting (Optional)'), blank=True)
    photo = models.ImageField(_('Upload a Photo (Optional)'), upload_to='tree_planting_submissions/', null=True, blank=True)
    agreement = models.BooleanField(_('Agreement/Consent'))
    submitted_at = models.DateTimeField(_('Submitted At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Tree Planting Submission')
        verbose_name_plural = _('Tree Planting Submissions')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.full_name} - {self.tree_type} ({self.quantity}) on {self.planting_date}"
from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Tree(models.Model):
    TREE_SPECIES = [
        ('coffee', _('Coffee Plant')),
        ('avocado', _('Avocado')),
        ('banana', _('Banana')),
        ('grevillea', _('Grevillea')),
        ('eucalyptus', _('Eucalyptus')),
    ]
    
    tree_id = models.CharField(_('Tree ID'), max_length=50, unique=True)
    species = models.CharField(_('Species'), max_length=100, choices=TREE_SPECIES)
    planted_date = models.DateField(_('Planted Date'))
    location = models.CharField(_('Location'), max_length=255, blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    planted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Planted By'),
        related_name='planted_trees'
    )
    farmer = models.ForeignKey(
        'farmers.Farmer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Farmer'),
        related_name='trees'
    )
    photo = models.ImageField(
        _('Photo'), 
        upload_to='trees/', 
        null=True, 
        blank=True
    )
    video = models.FileField(
        _('Video'),
        upload_to='trees/videos/',
        null=True,
        blank=True,
        help_text=_('Upload a short video (mp4, mov, webm, max 50MB)')
    )
    co2_offset = models.DecimalField(
        _('CO₂ Offset (kg)'), 
        max_digits=10, 
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Tree')
        verbose_name_plural = _('Trees')
        ordering = ['-planted_date']
    
    def __str__(self):
        return f"Tree {self.tree_id} ({self.get_species_display()})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('trees:detail', kwargs={'pk': self.pk})