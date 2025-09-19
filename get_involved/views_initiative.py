
from django.shortcuts import render, redirect
from .models import Partner
from .forms_initiative import PartnerForm, InitiativeJoinForm

def thank_you(request):
    return render(request, 'get_involved/thank_you.html')

def join_initiative(request):
    if request.method == 'POST':
        form = InitiativeJoinForm(request.POST, request.FILES)
        if form.is_valid():
            join = form.save()
            # Send admin notification email
            from django.core.mail import send_mail
            from django.conf import settings
            subject = f"New Initiative Join: {join.full_name or join.org_contact_person or 'Anonymous'}"
            message = f"""
New Initiative Join Submission
-----------------------------
Joining As: {join.join_as}
Full Name: {join.full_name}
Organization: {join.org_name}
Contact Person: {join.org_contact_person}
Email: {join.email}
Phone: {join.phone}
Country: {join.country}
Province: {join.province}
District: {join.district}
Purpose/Role: {join.purpose}
Amount: {join.amount if join.amount else 'N/A'}
Dedication Message: {join.dedication_message}
Motivation: {join.motivation}
Skills: {join.skills}
Interests: {join.interests}
Availability: {join.availability}
Preferred Location: {join.preferred_location}
Area of Expertise: {join.area_of_expertise}
Willing to Mentor: {'Yes' if join.willing_to_mentor else 'No'}
Resources to Offer: {join.resources_to_offer}
Barista Experience: {join.barista_experience}
Preferred Training: {join.preferred_training}
Consent: {'Yes' if join.consent else 'No'}
Submitted At: {join.submitted_at}
-----------------------------
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_NOTIFICATION_EMAIL]
            )
            return render(request, 'get_involved/join.html', {'form': InitiativeJoinForm(), 'success': True})
    else:
        form = InitiativeJoinForm()
    return render(request, 'get_involved/join.html', {'form': form})

def get_involved(request):
    return render(request, 'get_involved/get_involved.html')

def partners(request):
    partners = Partner.objects.filter(is_active=True)
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('get_involved:thank_you')
    else:
        form = PartnerForm()
    return render(request, 'get_involved/partners.html', {
        'partners': partners,
        'form': form,
    })

# The donate view and DonationForm are removed as the Donation model is now only in core. Use the core donation system for all donation logic.
