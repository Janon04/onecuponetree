from django.contrib import admin
from .models import Partner, InitiativeJoin

@admin.register(InitiativeJoin)
class InitiativeJoinAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'join_as', 'purpose', 'email', 'phone', 'submitted_at')
	list_filter = ('join_as', 'purpose', 'country', 'submitted_at')
	search_fields = ('full_name', 'org_name', 'email', 'phone', 'national_id', 'org_registration')
	readonly_fields = ('submitted_at',)
	fieldsets = (
		('General', {
			'fields': ('join_as', 'purpose', 'motivation', 'consent', 'submitted_at')
		}),
		('Individual Info', {
			'fields': ('full_name', 'gender', 'date_of_birth', 'nationality', 'national_id', 'occupation', 'profile_photo'),
			'classes': ('collapse',)
		}),
		('Organization Info', {
			'fields': ('org_name', 'org_registration', 'org_type', 'org_contact_person', 'org_website', 'org_logo'),
			'classes': ('collapse',)
		}),
		('Contact', {
			'fields': ('email', 'phone', 'country', 'province', 'district', 'sector', 'cell', 'village', 'how_heard')
		}),
		('Purpose Details', {
			'fields': ('skills', 'interests', 'availability', 'amount', 'preferred_location', 'dedication_message', 'area_of_expertise', 'willing_to_mentor', 'resources_to_offer', 'barista_experience', 'preferred_training')
		}),
	)

admin.site.register(Partner)
