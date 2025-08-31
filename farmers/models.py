# --- All imports at the top ---
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from datetime import timedelta

# --- Farmer Support Activity Model ---
class FarmerSupportActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('training', _('Training & Education')),
        ('input', _('Input Distribution')),
        ('technical', _('Technical Assistance')),
        ('market', _('Market Access')),
        ('financial', _('Financial Support')),
        ('monitoring', _('Monitoring & Evaluation')),
        ('community', _('Community Building')),
        ('health', _('Health & Wellbeing')),
        ('other', _('Other')),
    ]
    activity_type = models.CharField(_('Activity Type'), max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    date = models.DateField(_('Date'))
    location = models.CharField(_('Location'), max_length=100, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_activities')
    farmers = models.ManyToManyField('Farmer', blank=True, related_name='support_activities')
    outcome = models.TextField(_('Outcome/Notes'), blank=True)
    attachment = models.FileField(_('Attachment (photo, doc, etc.)'), upload_to='support_activities/', blank=True, null=True)
    is_public = models.BooleanField(_('Show on public site'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Farmer Support Activity')
        verbose_name_plural = _('Farmer Support Activities')
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title} ({self.date})"


# helper: today in UTC+2
def today_utc_plus_2():
    return timezone.now() + timedelta(hours=2)


# Section A & B: Household Identification & Head Information
class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    household_id = models.CharField(
        _('Household ID'),
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        help_text=_('16 digit household ID'),
    )
    VILLAGE_CELL_CHOICES = [
        ('village1', _('Village 1')),
        ('village2', _('Village 2')),
        ('village3', _('Village 3')),
    ]
    SECTOR_DISTRICT_CHOICES = [
        ('sector1', _('Sector 1')),
        ('sector2', _('Sector 2')),
        ('sector3', _('Sector 3')),
    ]
    village_cell = models.CharField(_('Village/Cell'), max_length=100, choices=VILLAGE_CELL_CHOICES)
    sector_district = models.CharField(_('Sector/District'), max_length=100, choices=SECTOR_DISTRICT_CHOICES)
    interview_date = models.DateField(
        _('Date of interview'),
        default=today_utc_plus_2,  # ✅ default today UTC+2
    )
    interviewer_name = models.CharField(_('Interviewer name'), max_length=100)

    # Head of household
    full_name = models.CharField(_('Full Name'), max_length=100, null=True, blank=True)
    SEX_CHOICES = (('M', _('Male')), ('F', _('Female')))
    sex = models.CharField(_('Sex'), max_length=1, choices=SEX_CHOICES)
    age = models.PositiveIntegerField(_('Age'), default=18)

    MARITAL_STATUS_CHOICES = (
        ('single', _('Single')),
        ('married', _('Married')),
        ('widowed', _('Widowed')),
        ('divorced', _('Divorced')),
    )
    marital_status = models.CharField(_('Marital Status'), max_length=10, choices=MARITAL_STATUS_CHOICES)

    EDUCATION_LEVEL_CHOICES = (
        ('none', _('None')),
        ('primary', _('Primary')),
        ('secondary', _('Secondary')),
        ('tertiary', _('Tertiary')),
    )
    education_level = models.CharField(
        _('Education Level'),
        max_length=10,
        choices=EDUCATION_LEVEL_CHOICES,
        default='none',
    )
    OCCUPATION_CHOICES = [
        ('farmer', _('Farmer')),
        ('teacher', _('Teacher')),
        ('trader', _('Trader')),
        ('other', _('Other')),
    ]
    occupation = models.CharField(_('Occupation/Income Source'), max_length=100, choices=OCCUPATION_CHOICES)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)

    # Section D: Education of Children
    num_children_school_age = models.PositiveIntegerField(_('Number of children of school age'), default=0)
    num_children_attending_school = models.PositiveIntegerField(_('Number currently attending school'), default=0)
    barrier_school_fees = models.BooleanField(_('Barrier: School fees'), default=False)
    barrier_lack_materials = models.BooleanField(_('Barrier: Lack of materials'), default=False)
    barrier_distance = models.BooleanField(_('Barrier: Distance to school'), default=False)
    barrier_early_marriage = models.BooleanField(_('Barrier: Early marriage/pregnancy'), default=False)
    barrier_other = models.CharField(_('Barrier: Other'), max_length=100, blank=True)

    # Section E: Livelihoods & Financial Stability
    INCOME_SOURCE_CHOICES = (
        ('farming', _('Farming')),
        ('livestock', _('Livestock')),
        ('business', _('Business')),
        ('employment', _('Employment (formal/informal)')),
        ('other', _('Other')),
    )
    main_income_source = models.CharField(_('Main source of income'), max_length=20, choices=INCOME_SOURCE_CHOICES)
    income_source_other = models.CharField(_('Other income source'), max_length=100, blank=True)
    avg_monthly_income = models.DecimalField(
        _('Average monthly income (RWF)'), max_digits=12, decimal_places=2, null=True, blank=True
    )
    has_savings = models.BooleanField(_('Do you have savings?'), default=False)
    has_loans = models.BooleanField(_('Do you have access to loans/credit?'), default=False)

    # Section F: Food Security & Nutrition
    MAIN_STAPLE_CHOICES = [
        ('maize', _('Maize')),
        ('beans', _('Beans')),
        ('cassava', _('Cassava')),
        ('rice', _('Rice')),
        ('other', _('Other')),
    ]
    main_staple_foods = models.CharField(_('Main staple foods'), max_length=100, choices=MAIN_STAPLE_CHOICES, blank=True)
    MEALS_PER_DAY_CHOICES = ((1, '1'), (2, '2'), (3, '3'))
    meals_per_day = models.PositiveSmallIntegerField(
        _('Meals eaten per day'), choices=MEALS_PER_DAY_CHOICES, default=2
    )
    food_shortage = models.BooleanField(_('Faced hunger/food shortage in last 3 months?'), default=False)
    FOOD_SHORTAGE_WHEN_CHOICES = [
        ('dry_season', _('Dry Season')),
        ('rainy_season', _('Rainy Season')),
        ('other', _('Other')),
    ]
    food_shortage_when = models.CharField(_('If yes, when?'), max_length=100, choices=FOOD_SHORTAGE_WHEN_CHOICES, blank=True)

    # Section G: Health & Sanitation
    nearest_health_facility = models.CharField(_('Nearest health facility'), max_length=100, blank=True)
    health_facility_distance_km = models.DecimalField(
        _('Health facility distance (km)'), max_digits=5, decimal_places=2, null=True, blank=True
    )
    has_chronic_illness = models.BooleanField(_('Any household member with chronic illness/disability?'), default=False)
    CHRONIC_ILLNESS_CHOICES = [
        ('none', _('None')),
        ('diabetes', _('Diabetes')),
        ('hiv', _('HIV/AIDS')),
        ('disability', _('Disability')),
        ('other', _('Other')),
    ]
    chronic_illness_details = models.CharField(_('Chronic illness/disability details'), max_length=100, choices=CHRONIC_ILLNESS_CHOICES, blank=True)
    WATER_SOURCE_CHOICES = (('tap', _('Tap')), ('borehole', _('Borehole')), ('river', _('River')), ('other', _('Other')))
    water_source = models.CharField(_('Water source'), max_length=10, choices=WATER_SOURCE_CHOICES)
    water_source_other = models.CharField(_('Other water source'), max_length=100, blank=True)
    TOILET_CHOICES = (('flush', _('Flush')), ('pit', _('Pit latrine')), ('none', _('None')))
    toilet_facility = models.CharField(_('Toilet facility'), max_length=10, choices=TOILET_CHOICES)

    # Section H: Housing Conditions
    HOUSE_TYPE_CHOICES = (
        ('permanent', _('Permanent')),
        ('semi', _('Semi-permanent')),
        ('temporary', _('Temporary')),
    )
    house_type = models.CharField(
        _('Type of house'), max_length=12, choices=HOUSE_TYPE_CHOICES, null=True, blank=True
    )
    ROOFING_CHOICES = (('iron', _('Iron sheets')), ('grass', _('Grass')), ('other', _('Other')))
    roofing = models.CharField(_('Roofing'), max_length=10, choices=ROOFING_CHOICES)
    roofing_other = models.CharField(_('Other roofing'), max_length=100, blank=True)
    LIGHTING_CHOICES = (
        ('electricity', _('Electricity')),
        ('solar', _('Solar')),
        ('kerosene', _('Kerosene')),
        ('other', _('Other')),
    )
    lighting_source = models.CharField(_('Lighting source'), max_length=12, choices=LIGHTING_CHOICES)
    lighting_other = models.CharField(_('Other lighting'), max_length=100, blank=True)

    # Section I: Community & Social Participation
    is_coop_member = models.BooleanField(_('Member of cooperative/association?'), default=False)
    is_savings_group_member = models.BooleanField(_('Member of savings group (IBIMINA)?'), default=False)
    has_support = models.BooleanField(_('Support received from government/NGOs?'), default=False)
    SUPPORT_DETAILS_CHOICES = [
        ('none', _('None')),
        ('govt', _('Government')),
        ('ngo', _('NGO')),
        ('community', _('Community')),
        ('other', _('Other')),
    ]
    support_details = models.CharField(_('Support details'), max_length=100, choices=SUPPORT_DETAILS_CHOICES, blank=True)

    # Legacy / optional fields
    location = models.CharField(_('location'), max_length=255, blank=True)
    farm_size = models.DecimalField(_('farm size (hectares)'), max_digits=10, decimal_places=2, null=True, blank=True)
    joined_date = models.DateField(_('joined date'), null=True, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='farmers/', null=True, blank=True)
    is_featured = models.BooleanField(_('is featured'), default=False)

    # timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Farmer')
        verbose_name_plural = _('Farmers')

    def __str__(self):
        return f"{self.full_name}" if self.full_name else super().__str__()

    def clean(self):
        if self.household_id and (len(self.household_id) != 16 or not self.household_id.isdigit()):
            from django.core.exceptions import ValidationError
            raise ValidationError({'household_id': _('Household ID must be exactly 16 digits.')})


# Section C: Household Composition
class HouseholdMember(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='household_members')
    name = models.CharField(_('Name'), max_length=100)
    relationship = models.CharField(_('Relationship to Head'), max_length=50)
    sex = models.CharField(_('Sex'), max_length=1, choices=Farmer.SEX_CHOICES)
    age = models.PositiveIntegerField(_('Age'), default=18)
    education_level = models.CharField(
        _('Education Level'), max_length=10, choices=Farmer.EDUCATION_LEVEL_CHOICES, default='none'
    )
    school_attendance = models.BooleanField(_('School Attendance'), default=False)
    main_occupation = models.CharField(_('Main Occupation'), max_length=100, blank=True)
    health_condition = models.CharField(_('Health Condition'), max_length=100, blank=True)
    notes = models.CharField(_('Notes'), max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


# Section E: Assets
class HouseholdAsset(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='assets')
    ASSET_TYPE_CHOICES = (('land', _('Land')), ('livestock', _('Livestock')), ('house', _('House')), ('other', _('Other')))
    asset_type = models.CharField(_('Asset Type'), max_length=20, choices=ASSET_TYPE_CHOICES)
    description = models.CharField(_('Description'), max_length=100, blank=True)
    quantity = models.CharField(_('Quantity/Size/Type'), max_length=100, blank=True)
    house_type = models.CharField(_('House Type'), max_length=12, choices=Farmer.HOUSE_TYPE_CHOICES, blank=True)

    def __str__(self):
        return f"{self.asset_type}: {self.description}"





# Farmer Stories
class FarmerStory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    photo = models.ImageField(_('photo'), upload_to='farmer_stories/', blank=True, null=True)
    video = models.FileField(_('video'), upload_to='farmer_stories/videos/', blank=True, null=True, help_text=_('Upload a short video (mp4, mov, webm, max 50MB)'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    is_published = models.BooleanField(_('is published'), default=True)

    class Meta:
        verbose_name = _('Farmer Story')
        verbose_name_plural = _('Farmer Stories')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.farmer}"
