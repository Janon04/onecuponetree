from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User
from django.utils import timezone

# -------------------------------
# Helper function for DateField default
# -------------------------------
def today_date():
    return timezone.now().date()


# -------------------------------
# Barista Training Models
# -------------------------------
class BaristaTraining(models.Model):
    title = models.CharField('Title', max_length=200)
    description = RichTextField('Description')
    date = models.DateField('Training date')
    location = models.CharField('Location', max_length=100)
    banner = models.ImageField(
        'Banner or pullup',
        upload_to='barista_training_banners/',
        blank=True,
        null=True
    )
    image = models.ImageField(
        'Image',
        upload_to='barista_training/images/',
        blank=True,
        null=True
    )
    video = models.FileField(
        'Video',
        upload_to='barista_training/videos/',
        blank=True,
        null=True,
        help_text='Upload a short video (mp4, mov, webm, max 50MB)'
    )
    is_active = models.BooleanField('Is active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Barista Training'
        verbose_name_plural = 'Barista Trainings'
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class BaristaTrainingApplication(models.Model):
    training = models.ForeignKey(
        BaristaTraining,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # 1. Personal Information
    full_name = models.CharField('Full Name', max_length=100)
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    age = models.PositiveIntegerField('Age')
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField('Gender', max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField('Nationality', max_length=50)
    id_number = models.CharField('National ID / Passport Number', max_length=50)

    # 2. Contact Information
    phone = models.CharField('Phone Number', max_length=30)
    email = models.EmailField('Email Address')
    country = models.CharField('Country', max_length=50)
    province = models.CharField('Province', max_length=50)
    district = models.CharField('District', max_length=50)
    sector = models.CharField('Sector', max_length=50)
    cell = models.CharField('Cell', max_length=50)
    village = models.CharField('Village', max_length=50)

    # 3. Educational & Professional Background
    education_level = models.CharField('Highest Level of Education Completed', max_length=100)
    occupation = models.CharField('Current Occupation / Employment Status', max_length=100)
    skills_experience = RichTextField('Relevant Skills or Experience', blank=True)

    # 4. Training-Specific Information
    motivation = RichTextField('Why do you want to attend this training?')
    expected_skills = RichTextField('What skills or knowledge do you expect to gain?', blank=True)
    attended_similar = models.BooleanField('Have you attended a similar training before?', default=False)
    attended_similar_details = models.CharField('If yes, please specify', max_length=200, blank=True)
    preferred_location = models.CharField('Preferred Training Location', max_length=100, blank=True)
    availability = models.CharField('Availability (days/times)', max_length=100, blank=True)

    # 5. Additional Information
    emergency_contact_name = models.CharField('Emergency Contact Name', max_length=100)
    emergency_contact_relationship = models.CharField('Relationship', max_length=50)
    emergency_contact_phone = models.CharField('Emergency Contact Phone', max_length=30)
    special_needs = models.CharField('Special Needs / Disabilities', max_length=200, blank=True)
    languages_spoken = models.CharField('Languages Spoken', max_length=100, blank=True)

    # 6. Declaration & Consent
    confirm_information = models.BooleanField('I confirm that the information provided is true and correct.')
    agree_participation = models.BooleanField('I agree to participate fully in the training program.')
    signature_name = models.CharField('Full Name of Applicant (as signature)', max_length=100)
    signature_date = models.DateField('Date', null=True, blank=True, default=today_date)

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barista Training Application'
        verbose_name_plural = 'Barista Training Applications'
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} - {self.training.title}"


# -------------------------------
# Volunteer Models
# -------------------------------
class VolunteerOpportunity(models.Model):
    title = models.CharField('Title', max_length=200)
    description = RichTextField('Description')
    location = models.CharField('Location', max_length=100)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date')
    skills_required = RichTextField('Skills required', blank=True)
    image = models.ImageField(
        'Image',
        upload_to='volunteer_opportunities/images/',
        blank=True,
        null=True,
        help_text='Upload an image (jpg, png, webp, max 5MB)'
    )
    video = models.FileField(
        'Video',
        upload_to='volunteer_opportunities/videos/',
        blank=True,
        null=True,
        help_text='Upload a short video (mp4, mov, webm, max 50MB)'
    )
    max_volunteers = models.PositiveIntegerField('Maximum volunteers', default=1)
    is_active = models.BooleanField('Is active', default=True)

    class Meta:
        verbose_name = 'Volunteer Opportunity'
        verbose_name_plural = 'Volunteer Opportunities'
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

    # 1. Personal Information
    full_name = models.CharField('Full Name', max_length=100)
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    gender = models.CharField(
        'Gender',
        max_length=10,
        choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other'))
    )
    id_number = models.CharField('National ID/Passport No.', max_length=16)
    phone = models.CharField('Phone Number', max_length=30)
    email = models.EmailField('Email Address')
    country = models.CharField('Country', max_length=50)
    province = models.CharField('Province/District', max_length=50)
    sector_cell_village = models.CharField('Sector/Cell/Village', max_length=100)

    # 2. Motivation Letter
    motivation = RichTextField('Motivation Letter')

    # 3. Relevant Skills & Experience
    skills = RichTextField('Relevant Skills & Experience')

    # 4. Availability
    availability_weekdays = models.CharField('Weekdays (specify times)', max_length=100, blank=True)
    availability_weekends = models.BooleanField('Weekends', default=False)
    availability_full_time = models.BooleanField('Full-time', default=False)
    availability_part_time = models.BooleanField('Part-time', default=False)
    availability_specific_dates = models.CharField('Specific dates', max_length=100, blank=True)

    # 5. Areas of Interest
    interest_community_outreach = models.BooleanField('Community Outreach', default=False)
    interest_event_support = models.BooleanField('Event Support', default=False)
    interest_training_mentorship = models.BooleanField('Training & Mentorship', default=False)
    interest_environmental = models.BooleanField('Environmental Activities (tree planting, farming, etc.)', default=False)
    interest_fundraising = models.BooleanField('Fundraising & Campaigns', default=False)
    interest_admin_support = models.BooleanField('Administrative Support', default=False)
    interest_other = models.CharField('Other', max_length=100, blank=True)

    # 6. Emergency Contact
    emergency_contact_name = models.CharField('Emergency Contact Name', max_length=100)
    emergency_contact_relationship = models.CharField('Relationship', max_length=50)
    emergency_contact_phone = models.CharField('Emergency Contact Phone', max_length=30)


    # 8. Declaration & Signature
    declaration = models.BooleanField('I confirm that the above information is true and complete.', default=False)
    signature_name = models.CharField('Signature (Full Name)', max_length=100)
    signature_date = models.DateField('Date', null=True, blank=True, default=today_date)

    # Relations
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    application_date = models.DateTimeField('Application date', auto_now_add=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = RichTextField('notes', blank=True)

    class Meta:
        verbose_name = 'Volunteer Application'
        verbose_name_plural = 'Volunteer Applications'
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.full_name} - {self.opportunity}"
