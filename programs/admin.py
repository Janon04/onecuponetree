from django.contrib import admin
from .models import Program

from django.utils.html import format_html

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active', 'created_at', 'media_preview')
	search_fields = ('name', 'description')
	list_filter = ('is_active',)

	readonly_fields = ('media_preview',)

	def media_preview(self, obj):
		if obj.video:
			return format_html('''
				<a href=\"#\" onclick=\"var vid=this.nextElementSibling; vid.style.display='block'; this.style.display='none'; return false;\">Show Video</a>
				<video width=\"120\" controls style=\"display:none; margin-top:8px; object-fit:cover;\"><source src=\"{}\" type=\"video/mp4\">Your browser does not support the video tag.</video>
			''', obj.video.url)
		elif obj.image:
			return format_html('''
				<a href=\"#\" onclick=\"var img=this.nextElementSibling; img.style.display='block'; this.style.display='none'; return false;\">Show Photo</a>
				<img src=\"{}\" width=\"120\" style=\"display:none; margin-top:8px; object-fit:cover;\" />
			''', obj.image.url)
		return ""
	media_preview.short_description = 'Media Preview'
