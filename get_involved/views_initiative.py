
from django.shortcuts import render, redirect
from .models import Partner
from .forms_initiative import PartnerForm, InitiativeJoinForm

def thank_you(request):
    return render(request, 'get_involved/thank_you.html')

def join_initiative(request):
    if request.method == 'POST':
        form = InitiativeJoinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
