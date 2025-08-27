from django.shortcuts import render, redirect
from .models import Partner, Volunteer, Donation
from .forms import VolunteerForm, DonationForm, PartnerForm

def get_involved(request):
    return render(request, 'get_involved/get_involved.html')

def join_initiative(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            if request.user.is_authenticated:
                volunteer.user = request.user
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

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.donor = request.user
            donation.save()
            return redirect('get_involved:thank_you')
    else:
        form = DonationForm()
    return render(request, 'get_involved/donate.html', {'form': form})