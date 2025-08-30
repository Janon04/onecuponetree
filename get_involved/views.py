def thank_you(request):
    return render(request, 'get_involved/thank_you.html')
from django.shortcuts import render, redirect
from .models import Partner, Volunteer
from .forms import VolunteerForm, PartnerForm

def get_involved(request):
    return render(request, 'get_involved/get_involved.html')

def join_initiative(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            if request.user.is_authenticated:
                volunteer.user = request.user
            # If not authenticated, user remains None (anonymous)
            volunteer.save()
            return redirect('get_involved:thank_you')
    else:
        form = VolunteerForm()
    return render(request, 'get_involved/join.html', {'form': form})

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

def volunteers(request):
    volunteers = Volunteer.objects.filter(is_active=True)
    return render(request, 'get_involved/volunteers.html', {'volunteers': volunteers})

# The donate view and DonationForm are removed as the Donation model is now only in core. Use the core donation system for all donation logic.