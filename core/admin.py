from django.contrib import admin
from .models import Contact, Donation
import csv
from django.http import HttpResponse

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'created_at')
	search_fields = ('name', 'email', 'subject')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
	list_display = ('donor_name', 'donor_email', 'amount', 'donation_type', 'payment_status', 'created_at')
	list_filter = ('donation_type', 'payment_status', 'created_at')
	search_fields = ('donor_name', 'donor_email', 'message')
	actions = ['export_as_csv']

	def export_as_csv(self, request, queryset):
		meta = self.model._meta
		field_names = [field.name for field in meta.fields]
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = f'attachment; filename=donations.csv'
		writer = csv.writer(response)
		writer.writerow(field_names)
		for obj in queryset:
			writer.writerow([getattr(obj, field) for field in field_names])
		return response
	export_as_csv.short_description = "Export Selected as CSV"
