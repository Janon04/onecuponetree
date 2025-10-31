from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import BlogPost, BlogCategory
import csv
from django.http import HttpResponse

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'posts_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def posts_count(self, obj):
        count = obj.blogpost_set.count()
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{} posts</span>',
            count
        )
    posts_count.short_description = "Posts"

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author_name', 'category', 'publication_status', 
        'pinned_status', 'media_preview', 'views_count', 'created_at'
    )
    list_filter = ('is_published', 'pinned', 'category', 'created_at', 'author')
    search_fields = ('title', 'description', 'content', 'author__username', 'author__first_name', 'author__last_name')
    readonly_fields = ('media_preview', 'content_stats', 'slug_preview')
    list_editable = ('pinned', 'is_published')
    date_hierarchy = 'created_at'
    ordering = ['-pinned', '-created_at']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Publication Settings', {
            'fields': ('is_published', 'pinned'),
            'classes': ('wide',)
        }),
        ('Basic Information', {
            'fields': ('title', 'slug', 'slug_preview', 'author', 'category', 'description')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Media', {
            'fields': ('featured_image', 'video', 'media_preview'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('content_stats',),
            'classes': ('collapse',)
        }),
    )
    
    def author_name(self, obj):
        if obj.author:
            full_name = obj.author.get_full_name()
            return full_name if full_name else obj.author.username
        return "No author"
    author_name.short_description = "Author"
    author_name.admin_order_field = 'author__username'
    
    def publication_status(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">'
                '<i class="fas fa-check"></i> Published</span>'
            )
        return format_html(
            '<span style="background: #ffc107; color: #212529; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">'
            '<i class="fas fa-clock"></i> Draft</span>'
        )
    publication_status.short_description = "Status"
    publication_status.admin_order_field = 'is_published'
    
    def pinned_status(self, obj):
        if obj.pinned:
            return format_html('<i class="fas fa-thumbtack" style="color: #d4af37; font-size: 16px;"></i>')
        return ""
    pinned_status.short_description = "📌"
    
    def media_preview(self, obj):
        html = []
        
        if obj.featured_image:
            html.append(
                f'<div style="margin-bottom: 10px;">'
                f'<img src="{obj.featured_image.url}" style="max-height: 80px; max-width: 120px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />'
                f'<div style="font-size: 11px; color: #666; margin-top: 2px;">Featured Image</div>'
                f'</div>'
            )
        
        if obj.video:
            html.append(
                f'<div style="margin-bottom: 10px;">'
                f'<div style="background: #17a2b8; color: white; padding: 6px 10px; border-radius: 4px; font-size: 11px; display: inline-block;">'
                f'<i class="fas fa-video"></i> Video Available'
                f'</div>'
                f'<div style="font-size: 11px; color: #666; margin-top: 2px;">Click to preview</div>'
                f'</div>'
            )
        
        if not html:
            html.append('<span style="color: #999; font-style: italic;">No media</span>')
        
        return format_html(''.join(html))
    media_preview.short_description = "Media"
    
    def views_count(self, obj):
        # Placeholder for future view tracking
        return format_html(
            '<span style="color: #666; font-size: 12px;"><i class="fas fa-eye"></i> N/A</span>'
        )
    views_count.short_description = "Views"
    
    def content_stats(self, obj):
        word_count = len(obj.content.split()) if obj.content else 0
        char_count = len(obj.content) if obj.content else 0
        
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">'
            '<strong>Content Statistics:</strong><br>'
            'Words: {:,}<br>'
            'Characters: {:,}<br>'
            'Description Length: {} chars<br>'
            'Estimated Reading Time: {} min'
            '</div>',
            word_count, char_count, 
            len(obj.description) if obj.description else 0,
            max(1, word_count // 200)  # Rough estimate: 200 words per minute
        )
    content_stats.short_description = "Content Analysis"
    
    def slug_preview(self, obj):
        if obj.slug:
            return format_html(
                '<div style="background: #e9ecef; padding: 8px; border-radius: 4px; font-family: monospace; font-size: 13px;">'
                'URL: /blog/{}/</div>',
                obj.slug
            )
        return "Will be auto-generated"
    slug_preview.short_description = "URL Preview"
    
    actions = ['publish_posts', 'unpublish_posts', 'pin_posts', 'unpin_posts', 'export_as_csv']
    
    def publish_posts(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} posts published successfully.')
    publish_posts.short_description = "Publish selected posts"
    
    def unpublish_posts(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} posts unpublished.')
    unpublish_posts.short_description = "Unpublish selected posts"
    
    def pin_posts(self, request, queryset):
        updated = queryset.update(pinned=True)
        self.message_user(request, f'{updated} posts pinned to top.')
    pin_posts.short_description = "Pin selected posts"
    
    def unpin_posts(self, request, queryset):
        updated = queryset.update(pinned=False)
        self.message_user(request, f'{updated} posts unpinned.')
    unpin_posts.short_description = "Unpin selected posts"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=blog_posts_{queryset.count()}_items.csv'
        writer = csv.writer(response)
        
        headers = [
            'Title', 'Author', 'Category', 'Description', 'Published', 'Pinned',
            'Created Date', 'Updated Date', 'Word Count', 'Has Image', 'Has Video'
        ]
        writer.writerow(headers)
        
        for obj in queryset:
            word_count = len(obj.content.split()) if obj.content else 0
            writer.writerow([
                obj.title,
                obj.author.get_full_name() if obj.author else '',
                obj.category.name if obj.category else '',
                obj.description,
                'Yes' if obj.is_published else 'No',
                'Yes' if obj.pinned else 'No',
                obj.created_at.strftime('%Y-%m-%d %H:%M'),
                obj.updated_at.strftime('%Y-%m-%d %H:%M'),
                word_count,
                'Yes' if obj.featured_image else 'No',
                'Yes' if obj.video else 'No'
            ])
        return response
    export_as_csv.short_description = "Export selected posts as CSV"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/blog_admin.js',)