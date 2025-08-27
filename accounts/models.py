from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model with role-based permissions and profile enhancements."""

    USER_ROLES = [
        ('admin', _('Administrator')),
        ('partner', _('Partner')),
        ('donor', _('Donor')),
        ('volunteer', _('Volunteer')),
        ('visitor', _('Visitor')),
        ('student', _('Student')),
    ]

    role = models.CharField(
        max_length=20, 
        choices=USER_ROLES, 
        default='visitor',
        help_text=_('User role determines access permissions')
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True,
        help_text=_('Contact phone number')
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text=_('Date of birth for age verification')
    )
    profile_image = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True,
        help_text=_('Profile picture')
    )
    bio = models.TextField(
        blank=True,
        help_text=_('Short biography or description')
    )
    location = models.CharField(
        max_length=100, 
        blank=True,
        help_text=_('Current location or address')
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the user account is verified')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin' or self.is_superuser

    def is_partner(self):
        """Check if user has partner role"""
        return self.role == 'partner'

    def is_donor(self):
        """Check if user has donor role"""
        return self.role == 'donor'

    def is_volunteer(self):
        """Check if user has volunteer role"""
        return self.role == 'volunteer'

    def is_student(self):
        """Check if user has student role"""
        return self.role == 'student'


class Interest(models.Model):
    """User interests for better matching and recommendations"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Interest')
        verbose_name_plural = _('Interests')
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    """User skills for volunteer matching and program assignments"""

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})" if self.category else self.name


class UserProfile(models.Model):
    """Extended user profile information"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    organization = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Organization or company name')
    )
    website = models.URLField(
        blank=True,
        help_text=_('Personal or organization website')
    )
    social_media_links = models.JSONField(
        default=dict,
        help_text=_('Social media profile links')
    )
    interests = models.ManyToManyField(
        Interest,
        blank=True,
        help_text=_('Areas of interest')
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        help_text=_('Skills and expertise')
    )
    languages = models.JSONField(
        default=list,
        help_text=_('Languages spoken')
    )
    newsletter_subscribed = models.BooleanField(
        default=False,
        help_text=_('Subscribed to newsletter')
    )
    privacy_settings = models.JSONField(
        default=dict,
        help_text=_('Privacy and visibility settings')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"


class UserActivity(models.Model):
    """Track user activities for analytics and engagement"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(
        max_length=100,
        help_text=_('Type of activity performed')
    )
    activity_description = models.TextField(
        help_text=_('Detailed description of the activity')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text=_('IP address when activity occurred')
    )
    user_agent = models.TextField(
        blank=True,
        help_text=_('Browser user agent string')
    )
    additional_data = models.JSONField(
        default=dict,
        help_text=_('Additional activity metadata')
    )

    class Meta:
        verbose_name = _('User Activity')
        verbose_name_plural = _('User Activities')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"