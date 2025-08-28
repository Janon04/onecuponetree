from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber
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
