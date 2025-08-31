from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class BaristaTraining(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    date = models.DateField(_('training date'))
    location = models.CharField(_('location'), max_length=100)
    banner = models.ImageField(_('banner or pullup'), upload_to='barista_training_banners/', blank=True, null=True)
    image = models.ImageField(_('image'), upload_to='barista_training/images/', blank=True, null=True)
    video = models.FileField(_('video'), upload_to='barista_training/videos/', blank=True, null=True, help_text=_('Upload a short video (mp4, mov, webm, max 50MB)'))
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Barista Training')
        verbose_name_plural = _('Barista Trainings')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class BaristaTrainingApplication(models.Model):
    training = models.ForeignKey(BaristaTraining, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    # 1. Personal Information
    full_name = models.CharField(_('Full Name'), max_length=100)
    date_of_birth = models.DateField(_('Date of Birth'))
    age = models.PositiveIntegerField(_('Age'))
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    )
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(_('Nationality'), max_length=50)
    id_number = models.CharField(_('National ID / Passport Number'), max_length=50)

    # 2. Contact Information
    phone = models.CharField(_('Phone Number'), max_length=30)
    email = models.EmailField(_('Email Address'))
    country = models.CharField(_('Country'), max_length=50)
    province = models.CharField(_('Province'), max_length=50)
    district = models.CharField(_('District'), max_length=50)
    sector = models.CharField(_('Sector'), max_length=50)
    cell = models.CharField(_('Cell'), max_length=50)
    village = models.CharField(_('Village'), max_length=50)

    # 3. Educational & Professional Background
    education_level = models.CharField(_('Highest Level of Education Completed'), max_length=100)
    occupation = models.CharField(_('Current Occupation / Employment Status'), max_length=100)
    skills_experience = models.TextField(_('Relevant Skills or Experience'), blank=True)

    # 4. Training-Specific Information
    motivation = models.TextField(_('Why do you want to attend this training?'))
    expected_skills = models.TextField(_('What skills or knowledge do you expect to gain?'), blank=True)
    attended_similar = models.BooleanField(_('Have you attended a similar training before?'), default=False)
    attended_similar_details = models.CharField(_('If yes, please specify'), max_length=200, blank=True)
    preferred_location = models.CharField(_('Preferred Training Location'), max_length=100, blank=True)
    availability = models.CharField(_('Availability (days/times)'), max_length=100, blank=True)

    # 5. Additional Information
    emergency_contact_name = models.CharField(_('Emergency Contact Name'), max_length=100)
    emergency_contact_relationship = models.CharField(_('Relationship'), max_length=50)
    emergency_contact_phone = models.CharField(_('Emergency Contact Phone'), max_length=30)
    special_needs = models.CharField(_('Special Needs / Disabilities'), max_length=200, blank=True)
    languages_spoken = models.CharField(_('Languages Spoken'), max_length=100, blank=True)

    # 6. Declaration & Consent
    confirm_information = models.BooleanField(_('I confirm that the information provided is true and correct.'))
    agree_participation = models.BooleanField(_('I agree to participate fully in the training program.'))
    signature_name = models.CharField(_('Full Name of Applicant (as signature)'), max_length=100)
    signature_date = models.DateField(_('Date'))

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Barista Training Application')
        verbose_name_plural = _('Barista Training Applications')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} - {self.training.title}"
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class VolunteerOpportunity(models.Model):
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    location = models.CharField(_('location'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    skills_required = models.TextField(_('skills required'), blank=True)
    max_volunteers = models.PositiveIntegerField(_('maximum volunteers'), default=1)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Volunteer Opportunity')
        verbose_name_plural = _('Volunteer Opportunities')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title

class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_date = models.DateTimeField(_('application date'), auto_now_add=True)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('Volunteer Application')
        verbose_name_plural = _('Volunteer Applications')
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.user} - {self.opportunity}"