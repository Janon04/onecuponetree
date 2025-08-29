
from django.contrib import admin
from .models import Farmer, HouseholdMember, HouseholdAsset, FarmerSupportActivity, FarmerStory

class HouseholdMemberInline(admin.TabularInline):
	model = HouseholdMember
	extra = 1

class HouseholdAssetInline(admin.TabularInline):
	model = HouseholdAsset
	extra = 1

class FarmerSupportActivityInline(admin.TabularInline):
	model = FarmerSupportActivity
	extra = 1

class FarmerStoryInline(admin.TabularInline):
	model = FarmerStory
	extra = 1

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
	list_display = ("full_name", "household_id", "village_cell", "sector_district", "phone_number", "main_income_source", "is_coop_member")
	search_fields = ("full_name", "household_id", "phone_number", "village_cell", "sector_district")
	inlines = [HouseholdMemberInline, HouseholdAssetInline, FarmerSupportActivityInline, FarmerStoryInline]
	from .forms import FarmerForm
	form = FarmerForm

@admin.register(HouseholdMember)
class HouseholdMemberAdmin(admin.ModelAdmin):
	list_display = ("name", "relationship", "sex", "age", "education_level", "school_attendance", "main_occupation", "farmer")
	search_fields = ("name", "relationship", "main_occupation")

@admin.register(HouseholdAsset)
class HouseholdAssetAdmin(admin.ModelAdmin):
	list_display = ("asset_type", "description", "quantity", "house_type", "farmer")
	search_fields = ("description", "asset_type")

@admin.register(FarmerSupportActivity)
class FarmerSupportActivityAdmin(admin.ModelAdmin):
	list_display = ("title", "farmer", "date", "support_type", "is_successful")
	search_fields = ("title", "support_type", "farmer__full_name")

@admin.register(FarmerStory)
class FarmerStoryAdmin(admin.ModelAdmin):
	list_display = ("title", "farmer", "created_at", "is_published")
	search_fields = ("title", "farmer__full_name")
