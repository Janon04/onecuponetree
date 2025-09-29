from django.contrib import admin
from .models import VolunteerOpportunity, VolunteerApplication, BaristaTraining, BaristaTrainingApplication
from django.utils.html import format_html

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'location', 'is_active', 'media_preview')
	search_fields = ('title', 'description', 'location')
	list_filter = ('is_active', 'start_date')
	readonly_fields = ('media_preview',)

	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="120" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.image:
			return format_html('''
				<a href=\"#\" onclick=\"var img=this.nextElementSibling; img.style.display='block'; this.style.display='none'; return false;\">Show Photo</a>
				<img src=\"{}\" width=\"120\" style=\"display:none; margin-top:8px; object-fit:cover;\" />
			''', obj.image.url)
		return ""
	media_preview.short_description = 'Media Preview'

admin.site.register(VolunteerApplication)
from django.utils.html import format_html

@admin.register(BaristaTraining)
class BaristaTrainingAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'location', 'is_active', 'media_preview')
	search_fields = ('title', 'description', 'location')
	list_filter = ('is_active', 'date')
	readonly_fields = ('media_preview',)

	def media_preview(self, obj):
		if obj.video:
			return format_html('<video width="120" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
		elif obj.image:
			return format_html('''
				<a href=\"#\" onclick=\"var img=this.nextElementSibling; img.style.display='block'; this.style.display='none'; return false;\">Show Photo</a>
				<img src=\"{}\" width=\"120\" style=\"display:none; margin-top:8px; object-fit:cover;\" />
			''', obj.image.url)
		elif obj.banner:
			return format_html('''
				<a href=\"#\" onclick=\"var img=this.nextElementSibling; img.style.display='block'; this.style.display='none'; return false;\">Show Photo</a>
				<img src=\"{}\" width=\"120\" style=\"display:none; margin-top:8px; object-fit:cover;\" />
			''', obj.banner.url)
		return ""
	media_preview.short_description = 'Media Preview'
@admin.register(BaristaTrainingApplication)
class BaristaTrainingApplicationAdmin(admin.ModelAdmin):
	def display_languages_spoken(self, obj):
		val = obj.languages_spoken
		if not val:
			return '-'
		# Remove brackets if present and split by comma
		if isinstance(val, str):
			val = val.strip('[]')
			items = [v.strip().strip("'").strip('"') for v in val.split(',') if v.strip()]
			return ', '.join(items)
		return str(val)
	display_languages_spoken.short_description = 'Languages Spoken'
	import openpyxl
	from django.http import HttpResponse

	def export_to_excel(self, request, queryset):
		wb = self.openpyxl.Workbook()
		ws = wb.active
		ws.title = "Applications"
		# Header
		ws.append([
			"ID", "Full Name", "Email", "Phone", "Motivation(s)", "Expected Skills", "Skills/Experience", "Languages Spoken"
		])
		for obj in queryset:
			ws.append([
				obj.id,
				obj.full_name,
				obj.email,
				obj.phone,
				', '.join([m.label for m in obj.motivation.all()]),
				', '.join([s.label for s in obj.expected_skills.all()]),
				', '.join([sk.label for sk in obj.skills_experience.all()]),
				obj.languages_spoken,
			])
		response = self.HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename=barista_training_applications.xlsx'
		wb.save(response)
		return response

	actions = ["export_to_excel"]
	list_display = [
		'id', 'full_name', 'email', 'phone', 'selected_for_training', 'display_motivation', 'display_expected_skills', 'display_skills_experience', 'display_languages_spoken',
	]
	def display_skills_experience(self, obj):
		items = obj.skills_experience.all()
		labels = [item.label for item in items]
		if labels:
			return ', '.join(labels)
		return '-'
	display_skills_experience.short_description = 'Skills/Experience'
	list_editable = ['selected_for_training']
	list_filter = ['selected_for_training']
	search_fields = ['full_name', 'email', 'phone']

	def display_motivation(self, obj):
		items = obj.motivation.all()
		labels = [item.label for item in items]
		if labels:
			return ', '.join(labels)
		return '-'
	display_motivation.short_description = 'Motivation(s)'

	def display_expected_skills(self, obj):
		items = obj.expected_skills.all()
		labels = [item.label for item in items]
		if labels:
			return ', '.join(labels)
		return '-'
	display_expected_skills.short_description = 'Expected Skills'