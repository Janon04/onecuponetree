# --- All imports at the top ---
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from accounts.models import User
from datetime import timedelta
from ckeditor.fields import RichTextField

# --- Farmer Support Activity Model ---
class FarmerSupportActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('training', 'Training & Education'),
        ('input', 'Input Distribution'),
        ('technical', 'Technical Assistance'),
        ('market', 'Market Access'),
        ('financial', 'Financial Support'),
        ('monitoring', 'Monitoring & Evaluation'),
        ('community', 'Community Building'),
        ('health', 'Health & Wellbeing'),
        ('other', 'Other'),
    ]
    activity_type = models.CharField('Activity Type', max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    title = models.CharField('Title', max_length=200)
    description = RichTextField('Description')
    date = models.DateField('Date')
    location = models.CharField('Location', max_length=100, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_activities')
    farmers = models.ManyToManyField('Farmer', blank=True, related_name='support_activities')
    outcome = RichTextField('Outcome/Notes', blank=True)
    attachment = models.FileField('Attachment (photo, doc, etc.)', upload_to='support_activities/', blank=True, null=True)
    is_public = models.BooleanField('Show on public site', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Farmer Support Activity'
        verbose_name_plural = 'Farmer Support Activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title} ({self.date})"


# helper: today in UTC+2
def today_utc_plus_2():
    return timezone.now() + timedelta(hours=2)


# Section A & B: Household Identification & Head Information
class Farmer(models.Model):
    # --- Sponsor a Farm fields ---
    sponsorship_goal = models.DecimalField('Sponsorship Goal (USD)', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Target amount for farm sponsorship')
    sponsorship_received = models.DecimalField('Sponsorship Received (USD)', max_digits=10, decimal_places=2, default=0, help_text='Total amount received for sponsorship')
    from ckeditor.fields import RichTextField
    sponsorship_description = RichTextField('Sponsorship Description', blank=True, help_text='Public info for sponsors')
    sponsorship_is_active = models.BooleanField('Sponsorship Active', default=False, help_text='Is this farm open for sponsorship?')
    sponsorship_logo = models.ImageField('Sponsorship Logo', upload_to='farm_sponsorships/logos/', blank=True, null=True)
    sponsorship_video = models.FileField('Sponsorship Video', upload_to='farm_sponsorships/videos/', blank=True, null=True, help_text='Optional video for sponsors')

    def sponsorship_progress(self):
        if self.sponsorship_goal and self.sponsorship_goal > 0:
            return min(100, int((self.sponsorship_received / self.sponsorship_goal) * 100))
        return 0
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    household_id = models.CharField(
        'Household ID',
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        help_text='16 digit household ID',
    )
    VILLAGE_CELL_CHOICES = [
        ('village1', 'Village 1'),
        ('village2', 'Village 2'),
        ('village3', 'Village 3'),
    ]
    SECTOR_DISTRICT_CHOICES = [
        ('sector1', 'Sector 1'),
        ('sector2', 'Sector 2'),
        ('sector3', 'Sector 3'),
    ]
    village_cell = models.CharField('Village/Cell', max_length=100, choices=VILLAGE_CELL_CHOICES)
    sector_district = models.CharField('Sector/District', max_length=100, choices=SECTOR_DISTRICT_CHOICES)
    interview_date = models.DateField(
        'Date of interview',
        default=today_utc_plus_2,  # ✅ default today UTC+2
    )
    interviewer_name = models.CharField('Interviewer name', max_length=100)

    # Head of household
    full_name = models.CharField('Full Name', max_length=100, null=True, blank=True)
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    sex = models.CharField('Sex', max_length=1, choices=SEX_CHOICES)
    age = models.PositiveIntegerField('Age', default=18)

    MARITAL_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
    )
    marital_status = models.CharField('Marital Status', max_length=10, choices=MARITAL_STATUS_CHOICES)

    EDUCATION_LEVEL_CHOICES = (
        ('none', 'None'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tertiary', 'Tertiary'),
    )
    education_level = models.CharField(
        'Education Level',
        max_length=10,
        choices=EDUCATION_LEVEL_CHOICES,
        default='none',
    )
    OCCUPATION_CHOICES = [
        ('farmer', 'Farmer'),
        ('teacher', 'Teacher'),
        ('trader', 'Trader'),
        ('other', 'Other'),
    ]
    occupation = models.CharField('Occupation/Income Source', max_length=100, choices=OCCUPATION_CHOICES)
    phone_number = models.CharField('Phone Number', max_length=20, blank=True)

    # Section D: Education of Children
    num_children_school_age = models.PositiveIntegerField('Number of children of school age', default=0)
    num_children_attending_school = models.PositiveIntegerField('Number currently attending school', default=0)
    barrier_school_fees = models.BooleanField('Barrier: School fees', default=False)
    barrier_lack_materials = models.BooleanField('Barrier: Lack of materials', default=False)
    barrier_distance = models.BooleanField('Barrier: Distance to school', default=False)
    barrier_early_marriage = models.BooleanField('Barrier: Early marriage/pregnancy', default=False)
    barrier_other = models.CharField('Barrier: Other', max_length=100, blank=True)

    # Section E: Livelihoods & Financial Stability
    INCOME_SOURCE_CHOICES = (
        ('farming', 'Farming'),
        ('livestock', 'Livestock'),
        ('business', 'Business'),
        ('employment', 'Employment (formal/informal)'),
        ('other', 'Other'),
    )
    main_income_source = models.CharField('Main source of income', max_length=20, choices=INCOME_SOURCE_CHOICES)
    income_source_other = models.CharField('Other income source', max_length=100, blank=True)
    avg_monthly_income = models.DecimalField(
        'Average monthly income (RWF)', max_digits=12, decimal_places=2, null=True, blank=True
    )
    has_savings = models.BooleanField('Do you have savings?', default=False)
    has_loans = models.BooleanField('Do you have access to loans/credit?', default=False)

    # Section F: Food Security & Nutrition
    MAIN_STAPLE_CHOICES = [
        ('maize', 'Maize'),
        ('beans', 'Beans'),
        ('cassava', 'Cassava'),
        ('rice', 'Rice'),
        ('other', 'Other'),
    ]
    main_staple_foods = models.CharField('Main staple foods', max_length=100, choices=MAIN_STAPLE_CHOICES, blank=True)
    MEALS_PER_DAY_CHOICES = ((1, '1'), (2, '2'), (3, '3'))
    meals_per_day = models.PositiveSmallIntegerField(
        'Meals eaten per day', choices=MEALS_PER_DAY_CHOICES, default=2
    )
    food_shortage = models.BooleanField('Faced hunger/food shortage in last 3 months?', default=False)
    FOOD_SHORTAGE_WHEN_CHOICES = [
        ('dry_season', 'Dry Season'),
        ('rainy_season', 'Rainy Season'),
        ('other', 'Other'),
    ]
    food_shortage_when = models.CharField('If yes, when?', max_length=100, choices=FOOD_SHORTAGE_WHEN_CHOICES, blank=True)

    # Section G: Health & Sanitation
    nearest_health_facility = models.CharField('Nearest health facility', max_length=100, blank=True)
    health_facility_distance_km = models.DecimalField(
        'Health facility distance (km)', max_digits=5, decimal_places=2, null=True, blank=True
    )
    has_chronic_illness = models.BooleanField('Any household member with chronic illness/disability?', default=False)
    CHRONIC_ILLNESS_CHOICES = [
        ('none', 'None'),
        ('diabetes', 'Diabetes'),
        ('hiv', 'HIV/AIDS'),
        ('disability', 'Disability'),
        ('other', 'Other'),
    ]
    chronic_illness_details = models.CharField('Chronic illness/disability details', max_length=100, choices=CHRONIC_ILLNESS_CHOICES, blank=True)
    WATER_SOURCE_CHOICES = (('tap', 'Tap'), ('borehole', 'Borehole'), ('river', 'River'), ('other', 'Other'))
    water_source = models.CharField('Water source', max_length=10, choices=WATER_SOURCE_CHOICES)
    water_source_other = models.CharField('Other water source', max_length=100, blank=True)
    TOILET_CHOICES = (('flush', 'Flush'), ('pit', 'Pit latrine'), ('none', 'None'))
    toilet_facility = models.CharField('Toilet facility', max_length=10, choices=TOILET_CHOICES)

    # Section H: Housing Conditions
    HOUSE_TYPE_CHOICES = (
        ('permanent', 'Permanent'),
        ('semi', 'Semi-permanent'),
        ('temporary', 'Temporary'),
    )
    house_type = models.CharField(
        'Type of house', max_length=12, choices=HOUSE_TYPE_CHOICES, null=True, blank=True
    )
    ROOFING_CHOICES = (('iron', 'Iron sheets'), ('grass', 'Grass'), ('other', 'Other'))
    roofing = models.CharField('Roofing', max_length=10, choices=ROOFING_CHOICES)
    roofing_other = models.CharField('Other roofing', max_length=100, blank=True)
    LIGHTING_CHOICES = (
        ('electricity', 'Electricity'),
        ('solar', 'Solar'),
        ('kerosene', 'Kerosene'),
        ('other', 'Other'),
    )
    lighting_source = models.CharField('Lighting source', max_length=12, choices=LIGHTING_CHOICES)
    lighting_other = models.CharField('Other lighting', max_length=100, blank=True)

    # Section I: Community & Social Participation
    is_coop_member = models.BooleanField('Member of cooperative/association?', default=False)
    is_savings_group_member = models.BooleanField('Member of savings group (IBIMINA)?', default=False)
    has_support = models.BooleanField('Support received from government/NGOs?', default=False)
    SUPPORT_DETAILS_CHOICES = [
        ('none', 'None'),
        ('govt', 'Government'),
        ('ngo', 'NGO'),
        ('community', 'Community'),
        ('other', 'Other'),
    ]
    support_details = models.CharField('Support details', max_length=100, choices=SUPPORT_DETAILS_CHOICES, blank=True)

    # Legacy / optional fields
    location = models.CharField('Location', max_length=255, blank=True)
    farm_size = models.DecimalField('Farm size (hectares)', max_digits=10, decimal_places=2, null=True, blank=True)
    joined_date = models.DateField('Joined date', null=True, blank=True)
    bio = RichTextField('Bio', blank=True)
    photo = models.ImageField('Photo', upload_to='farmers/', null=True, blank=True)
    is_featured = models.BooleanField('Is featured', default=False)

    # timestamps
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Farmer'
        verbose_name_plural = 'Farmers'

    def __str__(self):
        return f"{self.full_name}" if self.full_name else super().__str__()

    def clean(self):
        if self.household_id and (len(self.household_id) != 16 or not self.household_id.isdigit()):
            from django.core.exceptions import ValidationError
            raise ValidationError({'household_id': 'Household ID must be exactly 16 digits.'})


# Section C: Household Composition
class HouseholdMember(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='household_members')
    name = models.CharField('Name', max_length=100)
    relationship = models.CharField('Relationship to Head', max_length=50)
    sex = models.CharField('Sex', max_length=1, choices=Farmer.SEX_CHOICES)
    age = models.PositiveIntegerField('Age', default=18)
    education_level = models.CharField(
        'Education Level', max_length=10, choices=Farmer.EDUCATION_LEVEL_CHOICES, default='none'
    )
    school_attendance = models.BooleanField('School Attendance', default=False)
    main_occupation = models.CharField('Main Occupation', max_length=100, blank=True)
    health_condition = models.CharField('Health Condition', max_length=100, blank=True)
    notes = models.CharField('Notes', max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


# Section E: Assets
class HouseholdAsset(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='assets')
    ASSET_TYPE_CHOICES = (('land', 'Land'), ('livestock', 'Livestock'), ('house', 'House'), ('other', 'Other'))
    asset_type = models.CharField('Asset Type', max_length=20, choices=ASSET_TYPE_CHOICES)
    description = models.CharField('Description', max_length=100, blank=True)
    quantity = models.CharField('Quantity/Size/Type', max_length=100, blank=True)
    house_type = models.CharField('House Type', max_length=12, choices=Farmer.HOUSE_TYPE_CHOICES, blank=True)

    def __str__(self):
        return f"{self.asset_type}: {self.description}"





# Farmer Stories
class FarmerStory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField('Title', max_length=200)
    content = RichTextField('Content')
    photo = models.ImageField('Photo', upload_to='farmer_stories/', blank=True, null=True)
    video = models.FileField('Video', upload_to='farmer_stories/videos/', blank=True, null=True, help_text='Upload a short video (mp4, mov, webm, max 50MB)')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    is_published = models.BooleanField('Is published', default=True)

    class Meta:
        verbose_name = 'Farmer Story'
        verbose_name_plural = 'Farmer Stories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.farmer}"


# --- Sponsor a Farm models (moved from models_farm_sponsor.py) ---
class Farm(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="farm_images/", blank=True, null=True)
    video = models.FileField(upload_to="farm_videos/", blank=True, null=True)
    sponsorship_is_active = models.BooleanField(default=True, help_text="Is this farm open for sponsorship?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def total_sponsorship_amount(self):
        return sum(s.amount for s in self.sponsorships.filter(status='completed'))

    def sponsorship_count(self):
        return self.sponsorships.filter(status='completed').count()

class FarmSponsorship(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    farm = models.ForeignKey(Farm, related_name="sponsorships", on_delete=models.CASCADE)
    sponsor_name = models.CharField(max_length=255, blank=True, help_text="Optional public sponsor name")
    sponsor_email = models.EmailField(blank=True, help_text="For receipt/confirmation, not shown publicly")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = RichTextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sponsorship for {self.farm.name} - {self.amount} ({self.status})"
