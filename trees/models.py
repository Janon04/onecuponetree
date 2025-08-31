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