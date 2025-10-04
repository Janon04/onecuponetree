
from django.db import models

class TreePlantingSubmission(models.Model):
    reason = models.TextField('Reason for Planting (Optional)', blank=True, null=True)
    agreement = models.BooleanField('I commit to ensuring the planted trees are cared for and maintained.', default=False)
    TREE_TYPE_CHOICES = [
        ('mango', 'Mango'),
        ('coffee', 'Coffee'),
        ('eucalyptus', 'Eucalyptus'),
        ('avocado', 'Avocado'),
        ('other', 'Other'),
    ]
    CONTRIBUTION_TYPE_CHOICES = [
        ('self', 'I will provide and plant the trees myself 🌱'),
        ('donate', 'I will donate/provide trees for planting 🌳'),
        ('support', 'I will support others to plant trees (financial or logistical support) 💚'),
    ]

    tree_type = models.CharField('Tree Type', max_length=32, choices=TREE_TYPE_CHOICES)
    quantity = models.PositiveIntegerField('Quantity (Number of Trees)')
    country = models.CharField('Country', max_length=64)
    province = models.CharField('Province', max_length=64)
    district = models.CharField('District', max_length=64)
    sector = models.CharField('Sector', max_length=64)
    cell = models.CharField('Cell', max_length=64)
    village = models.CharField('Village', max_length=64)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, null=True, blank=True)
    planting_date = models.DateField('Planting Date')
    contribution_type = models.CharField('Contribution Type', max_length=32, choices=CONTRIBUTION_TYPE_CHOICES)
    full_name = models.CharField('Your Full Name', max_length=128)

    contact = models.CharField('Email Address / Phone Number', max_length=128)

    class Meta:
        verbose_name = 'Tree Planting Submission'
        verbose_name_plural = 'Tree Planting Submissions'
    # app_label removed

    def __str__(self):
        return f"{self.full_name} - {self.tree_type} ({self.quantity}) on {self.planting_date}"
from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Tree(models.Model):
    TREE_SPECIES = [
        ('coffee', 'Coffee Plant'),
        ('avocado', 'Avocado'),
        ('banana', 'Banana'),
        ('grevillea', 'Grevillea'),
        ('eucalyptus', 'Eucalyptus'),
    ]
    
    pinned = models.BooleanField('Pinned', default=False, help_text='Pin this tree to keep it at the top')
    tree_id = models.CharField('Tree ID', max_length=50, unique=True)
    species = models.CharField('Species', max_length=100, choices=TREE_SPECIES)
    planted_date = models.DateField('Planted Date')
    RWANDA_DISTRICTS = [
        ('Gasabo', 'Gasabo'), ('Kicukiro', 'Kicukiro'), ('Nyarugenge', 'Nyarugenge'),
        ('Bugesera', 'Bugesera'), ('Gatsibo', 'Gatsibo'), ('Kayonza', 'Kayonza'),
        ('Kirehe', 'Kirehe'), ('Ngoma', 'Ngoma'), ('Nyagatare', 'Nyagatare'),
        ('Rwamagana', 'Rwamagana'), ('Burera', 'Burera'), ('Gakenke', 'Gakenke'),
        ('Gicumbi', 'Gicumbi'), ('Musanze', 'Musanze'), ('Rulindo', 'Rulindo'),
        ('Gisagara', 'Gisagara'), ('Huye', 'Huye'), ('Kamonyi', 'Kamonyi'),
        ('Muhanga', 'Muhanga'), ('Nyamagabe', 'Nyamagabe'), ('Nyanza', 'Nyanza'),
        ('Ruhango', 'Ruhango'), ('Karongi', 'Karongi'), ('Ngororero', 'Ngororero'),
        ('Nyabihu', 'Nyabihu'), ('Rubavu', 'Rubavu'), ('Rusizi', 'Rusizi'), ('Rutsiro', 'Rutsiro')
    ]
    location = models.CharField('Location', max_length=255, choices=RWANDA_DISTRICTS, blank=True)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, default=0)
    planted_by = models.CharField('Planted By', max_length=128, blank=True)
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
    ordering = ['-pinned', '-planted_date']
    # app_label removed
    
    def __str__(self):
        return f"Tree {self.tree_id} ({self.get_species_display()})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('trees:detail', kwargs={'pk': self.pk})