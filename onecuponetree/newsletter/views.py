from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber, Newsletter
from django.shortcuts import render
def newsletter_list(request):
    newsletters = Newsletter.objects.filter(published=True).order_by('-created_at')
    return render(request, 'newsletter/newsletter_list.html', {'newsletters': newsletters})
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, _("Please enter a valid email address."))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        if NewsletterSubscriber.objects.filter(email__iexact=email).exists():
            messages.info(request, _("You are already subscribed to our newsletter."))
        else:
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, _("Thank you for subscribing to our newsletter!"))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
