from django.core.mail import send_mail
from django.conf import settings

def send_donation_thank_you(donation):
    if donation.donor_email:
        subject = 'Thank you for your donation!'
        message = f"Dear {donation.donor_name or 'Supporter'},\n\nThank you for your generous donation of {donation.amount} RWF to the One Cup Initiative.\n\nYour support is making a real difference!\n\nBest regards,\nOne Cup Initiative Team"
        send_mail(
            subject,
            message,
            settings.CONTACT_EMAIL,
            [donation.donor_email],
            fail_silently=True,
        )
        donation.receipt_sent = True
        donation.save()
