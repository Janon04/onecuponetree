
from django.contrib import admin
from .models import Product, Order, MockIremboPayGateway


from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "currency", "is_active", "image_tag")
	search_fields = ("name",)
	list_filter = ("currency",)

	def image_tag(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
		return ""
	image_tag.short_description = "Image"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "full_name", "email", "phone", "country", "city", "zip_code", "delivery_method", "total_amount", "status", "created_at")
	list_filter = ("status", "created_at", "delivery_method", "country")

@admin.register(MockIremboPayGateway)
class MockIremboPayGatewayAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active")
