
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
	inlines = [HouseholdMemberInline, HouseholdAssetInline, FarmerStoryInline]
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
	list_display = ("title", "activity_type", "date", "location", "staff", "is_public")
	list_filter = ("activity_type", "date", "is_public")
	search_fields = ("title", "description", "location", "outcome")
	filter_horizontal = ("farmers",)
	readonly_fields = ("created_at", "updated_at")

from django.utils.html import format_html

@admin.register(FarmerStory)
class FarmerStoryAdmin(admin.ModelAdmin):
	list_display = ("title", "farmer", "created_at", "is_published", "media_preview")
	search_fields = ("title", "farmer__full_name")
	readonly_fields = ("media_preview",)
	fieldsets = (
		(None, {
			'fields': ("farmer", "title", "content", "photo", "video", "media_preview", "is_published")
		}),
	)
	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="180" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.photo:
			return format_html('<img src="{}" width="120" />', obj.photo.url)
		return ""
	media_preview.short_description = 'Preview'
