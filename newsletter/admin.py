
from django.contrib import admin
from .models import NewsletterSubscriber, Newsletter, NewsletterMedia
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mass_mail
from django.utils import timezone
from django import forms
from ckeditor.widgets import CKEditorWidget

class NewsletterMediaInline(admin.TabularInline):
    model = NewsletterMedia
    extra = 1
    fields = ('image', 'video', 'media_preview', 'created_at')
    readonly_fields = ('media_preview', 'created_at')

    def media_preview(self, obj):
        if obj.video:
            return format_html('<video width="120" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        elif obj.image:
            return format_html('<img src="{}" width="120" style="object-fit:cover;" />', obj.image.url)
        return ""
    media_preview.short_description = 'Preview'

class NewsletterAdminForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    form = NewsletterAdminForm
    list_display = ('subject', 'has_document', 'created_at', 'published', 'sent_at', 'send_newsletter_action')
    list_filter = ('published', 'created_at', 'sent_at')
    search_fields = ('subject', 'description', 'content')
    actions = ['send_newsletter']
    inlines = [NewsletterMediaInline]
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('subject', 'description')
        }),
        (_('Content'), {
            'fields': ('content', 'document'),
            'description': _('You can either provide content or upload a document, or both. Content is optional.')
        }),
        (_('Publishing'), {
            'fields': ('published',)
        }),
    )
    
    def has_document(self, obj):
        if obj.document:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: gray;">✗ No</span>')
    has_document.short_description = _('Document')

    def send_newsletter_action(self, obj):
        if obj.published and not obj.sent_at:
            return format_html('<a class="button" href="../send_newsletter/{}/">{}</a>', obj.id, _('Send Now'))
        elif obj.sent_at:
            return _('Sent')
        return _('Draft')
    send_newsletter_action.short_description = _('Send Newsletter')

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            if newsletter.published and not newsletter.sent_at:
                subscribers = NewsletterSubscriber.objects.filter(is_active=True)
                recipient_list = [s.email for s in subscribers]
                if recipient_list:
                    send_mass_mail(((newsletter.subject, newsletter.content, None, recipient_list),), fail_silently=False)
                    newsletter.sent_at = timezone.now()
                    newsletter.save()
        self.message_user(request, _('Selected newsletters have been sent.'))
    send_newsletter.short_description = _('Send selected newsletters to all subscribers')

@admin.register(NewsletterMedia)
class NewsletterMediaAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'image', 'video', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active', 'subscribed_at')
