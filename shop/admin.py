from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Product, ProductCategory, ProductReview, Cart, CartItem, Order
import csv
from django.http import HttpResponse


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count_display', 'is_active', 'ordering')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'ordering')
    ordering = ['ordering', 'name']
    
    def product_count_display(self, obj):
        count = obj.product_count
        return format_html(
            '<span style="background: #007bff; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{} products</span>',
            count
        )
    product_count_display.short_description = "Products"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'rating_display', 'is_approved', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'comment', 'product__name')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'customer_name', 'customer_email', 'rating', 'comment')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 16px;">{}</span>',
            stars
        )
    rating_display.short_description = "Rating"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'stock_status', 'rating_display', 'image_preview', 'is_active', 'is_featured', 'is_new')
    list_filter = ('is_active', 'is_featured', 'is_new', 'category', 'currency')
    search_fields = ('name', 'description', 'slug')
    readonly_fields = ('image_preview', 'product_stats', 'slug', 'created_at', 'updated_at')
    list_editable = ('is_active', 'is_featured', 'is_new')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'category', 'description', 'image', 'image_preview')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'currency')
        }),
        ('Inventory', {
            'fields': ('stock_quantity',)
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_new')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('product_stats',),
            'classes': ('collapse',)
        }),
    )
    
    def stock_status(self, obj):
        if obj.stock_quantity > 10:
            color = '#28a745'
            icon = 'check-circle'
            text = f'In Stock ({obj.stock_quantity})'
        elif obj.stock_quantity > 0:
            color = '#ffc107'
            icon = 'exclamation-triangle'
            text = f'Low Stock ({obj.stock_quantity})'
        else:
            color = '#dc3545'
            icon = 'times-circle'
            text = 'Out of Stock'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
            '<i class="fas fa-{}"></i> {}</span>',
            color, icon, text
        )
    stock_status.short_description = "Stock"
    
    def rating_display(self, obj):
        if obj.average_rating:
            stars = '★' * int(obj.average_rating) + '☆' * (5 - int(obj.average_rating))
            return format_html(
                '<span style="color: #ffc107;">{}</span> <small>({} reviews)</small>',
                stars, obj.review_count
            )
        return format_html('<small style="color: #6c757d;">No reviews</small>')
    rating_display.short_description = "Rating"
    
    def price_display(self, obj):
        return format_html(
            '<span style="font-weight: 600; color: #28a745; font-size: 14px;">{} {}</span>',
            obj.currency, obj.price
        )
    price_display.short_description = "Price"
    price_display.admin_order_field = 'price'
    
    def availability_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
                '<i class="fas fa-check"></i> Available</span>'
            )
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
            '<i class="fas fa-times"></i> Unavailable</span>'
        )
    availability_status.short_description = "Status"
    availability_status.admin_order_field = 'is_active'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"
    
    def order_count(self, obj):
        count = CartItem.objects.filter(product=obj).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
        
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{} sold</span>',
            count
        )
    order_count.short_description = "Sales"
    
    def product_stats(self, obj):
        cart_items = CartItem.objects.filter(product=obj)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        cart_count = cart_items.values('cart').distinct().count()
        
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Product Statistics:</strong><br>'
            'Total Quantity Sold: {}<br>'
            'Number of Orders: {}<br>'
            'Average per Order: {:.1f}<br>'
            'Status: {}'
            '</div>',
            total_quantity, cart_count,
            total_quantity / cart_count if cart_count > 0 else 0,
            'Active' if obj.is_active else 'Inactive'
        )
    product_stats.short_description = "Product Analytics"
    
    actions = ['activate_products', 'deactivate_products', 'export_as_csv']
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    deactivate_products.short_description = "Deactivate selected products"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=products_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        
        headers = ['Name', 'Description', 'Price', 'Currency', 'Active', 'Total Sold']
        writer.writerow(headers)
        
        for obj in queryset:
            total_sold = CartItem.objects.filter(product=obj).aggregate(
                Sum('quantity')
            )['quantity__sum'] or 0
            
            writer.writerow([
                obj.name, obj.description, obj.price, obj.currency,
                'Yes' if obj.is_active else 'No', total_sold
            ])
        return response
    export_as_csv.short_description = "Export selected products as CSV"

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product_price', 'total_price')
    
    def product_price(self, obj):
        if obj.product:
            return f"{obj.product.currency} {obj.product.price}"
        return "N/A"
    product_price.short_description = "Unit Price"
    
    def total_price(self, obj):
        if obj.product:
            total = obj.quantity * obj.product.price
            return f"{obj.product.currency} {total}"
        return "N/A"
    total_price.short_description = "Total"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'items_count', 'total_value', 'created_at', 'status')
    list_filter = ('created_at',)
    search_fields = ('session_key',)
    readonly_fields = ('cart_summary',)
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    inlines = [CartItemInline]
    
    def items_count(self, obj):
        count = obj.items.count()
        total_quantity = obj.items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        return format_html(
            '<span style="font-weight: 600;">{} items</span><br>'
            '<span style="color: #666; font-size: 12px;">({} total quantity)</span>',
            count, total_quantity
        )
    items_count.short_description = "Items"
    
    def total_value(self, obj):
        total = 0
        currency = "RWF"  # Default currency
        
        for item in obj.items.all():
            if item.product:
                total += item.quantity * item.product.price
                currency = item.product.currency
        
        return format_html(
            '<span style="font-weight: 600; color: #28a745;">{} {}</span>',
            currency, total
        )
    total_value.short_description = "Total Value"
    
    def status(self, obj):
        # Check if cart has associated order
        has_order = hasattr(obj, 'order_set') and obj.order_set.exists()
        
        if has_order:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
                '<i class="fas fa-check"></i> Ordered</span>'
            )
        return format_html(
            '<span style="background: #ffc107; color: #212529; padding: 4px 8px; border-radius: 4px; font-size: 12px;">'
            '<i class="fas fa-shopping-cart"></i> Pending</span>'
        )
    status.short_description = "Status"
    
    def cart_summary(self, obj):
        items = obj.items.all()
        total_value = 0
        currency = "RWF"
        
        html = '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
        html += '<strong>Cart Summary:</strong><br>'
        
        for item in items:
            if item.product:
                item_total = item.quantity * item.product.price
                total_value += item_total
                currency = item.product.currency
                
                html += f'• {item.product.name}: {item.quantity} × {currency} {item.product.price} = {currency} {item_total}<br>'
        
        html += f'<hr style="margin: 8px 0;"><strong>Total: {currency} {total_value}</strong>'
        html += '</div>'
        
        return format_html(html)
    cart_summary.short_description = "Cart Details"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'cart_info', 'status_badge', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('order_summary', 'payment_info')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'country', 'city', 'zip_code', 'delivery_method')
        }),
        ('Order Details', {
            'fields': ('cart', 'status', 'total_amount')
        }),
        ('Payment Information', {
            'fields': ('payment_info',),
            'classes': ('collapse',)
        }),
        ('Order Summary', {
            'fields': ('order_summary',),
            'classes': ('collapse',)
        }),
    )
    
    def customer_info(self, obj):
        return format_html(
            '<div style="font-size: 13px;">'
            '<strong>{}</strong><br>'
            '<span style="color: #666;">{}</span><br>'
            '<span style="color: #666;">{}</span>'
            '</div>',
            obj.full_name or 'N/A',
            obj.email or 'N/A',
            obj.phone or 'N/A'
        )
    customer_info.short_description = "Customer"
    
    def cart_info(self, obj):
        if obj.cart:
            items_count = obj.cart.items.count()
            return format_html(
                '<span style="color: #17a2b8;">Cart #{}</span><br>'
                '<span style="color: #666; font-size: 12px;">{} items</span>',
                obj.cart.id, items_count
            )
        return "No cart"
    cart_info.short_description = "Cart"
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'paid': '#28a745',
            'failed': '#dc3545'
        }
        
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'status'
    
    def total_amount(self, obj):
        if obj.cart:
            total = 0
            currency = "RWF"
            
            for item in obj.cart.items.all():
                if item.product:
                    total += item.quantity * item.product.price
                    currency = item.product.currency
            
            return format_html(
                '<span style="font-weight: 600; color: #28a745; font-size: 14px;">{} {}</span>',
                currency, total
            )
        return "N/A"
    total_amount.short_description = "Total"
    
    def order_summary(self, obj):
        if not obj.cart:
            return "No cart associated"
        
        html = '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
        html += '<strong>Order Details:</strong><br>'
        
        total = 0
        currency = "RWF"
        
        for item in obj.cart.items.all():
            if item.product:
                item_total = item.quantity * item.product.price
                total += item_total
                currency = item.product.currency
                html += f'• {item.product.name}: {item.quantity} × {currency} {item.product.price} = {currency} {item_total}<br>'
        
        html += f'<hr style="margin: 8px 0;"><strong>Total: {currency} {total}</strong><br>'
        html += f'Status: {obj.get_status_display()}<br>'
        html += f'Created: {obj.created_at.strftime("%Y-%m-%d %H:%M")}'
        html += '</div>'
        
        return format_html(html)
    order_summary.short_description = "Order Summary"
    
    def payment_info(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Payment Information:</strong><br>'
            'Status: {}<br>'
            'Total Amount: {} {}<br>'
            'Delivery: {}'
            '</div>',
            obj.get_status_display(),
            obj.total_amount,
            'RWF',  # Assuming default currency
            obj.get_delivery_method_display()
        )
    payment_info.short_description = "Payment Details"
    
    actions = ['mark_as_paid', 'mark_as_failed', 'export_as_csv']
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = "Mark selected orders as paid"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} orders marked as failed.')
    mark_as_failed.short_description = "Mark selected orders as failed"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=orders_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        
        headers = [
            'Order ID', 'Customer Name', 'Customer Email', 'Customer Phone',
            'Status', 'Total Amount', 'Country', 'City', 'Created Date'
        ]
        writer.writerow(headers)
        
        for obj in queryset:
            total = obj.total_amount
            
            writer.writerow([
                obj.id, obj.full_name, obj.email, obj.phone,
                obj.get_status_display(), total, obj.country,
                obj.city, obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        return response
    export_as_csv.short_description = "Export selected orders as CSV"