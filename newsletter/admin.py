from django.contrib import admin
from .models import NewsletterSubscriber, Newsletter
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mass_mail
from django.utils import timezone
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'published', 'sent_at', 'send_newsletter_action')
    list_filter = ('published', 'created_at', 'sent_at')
    search_fields = ('subject', 'content')
    actions = ['send_newsletter']

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

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active', 'subscribed_at')
