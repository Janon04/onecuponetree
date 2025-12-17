from .models import FarmSponsorship
from .forms import FarmSponsorshipForm
from django.shortcuts import render, get_object_or_404
from .models import Farmer, FarmerStory, FarmerSupportActivity, Farm
from django.http import HttpResponseRedirect
from django.urls import reverse
def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk, is_active=True)
    goal = getattr(farm, 'sponsorship_goal', None)
    total = farm.total_sponsorship_amount() if hasattr(farm, 'total_sponsorship_amount') else 0
    if goal and goal > 0:
        sponsorship_progress = min(100, int((total / goal) * 100))
    else:
        sponsorship_progress = 0
    form = FarmSponsorshipForm(request.POST or None)
    form_success = False
    if request.method == 'POST' and farm.sponsorship_is_active:
        if form.is_valid():
            cd = form.cleaned_data
            FarmSponsorship.objects.create(
                farm=farm,
                sponsor_name=cd['sponsor_name'],
                sponsor_email=cd['sponsor_email'],
                amount=cd['amount'],
                message=cd['message'],
                status='pending',
            )
            form_success = True
            form = FarmSponsorshipForm()  # reset form
    return render(request, 'farmers/farm_detail.html', {
        'farm': farm,
        'sponsorship_progress': sponsorship_progress,
        'total_sponsorship_amount': total,
        'form': form,
        'form_success': form_success,
    })
def story_list(request):
    stories = FarmerStory.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'farmers/story_list.html', {'stories': stories})
def support_activities_public(request):
    activities = FarmerSupportActivity.objects.filter(is_public=True).order_by('-date')
    return render(request, 'farmers/support_activities_public.html', {'activities': activities})

# Sponsor a Farm: List all farms for sponsorship
def farm_list(request):
    farms = Farm.objects.filter(is_active=True)
    # Add sponsorship progress for each farm
    for farm in farms:
        goal = getattr(farm, 'sponsorship_goal', None)
        total = farm.total_sponsorship_amount() if hasattr(farm, 'total_sponsorship_amount') else 0
        if goal and goal > 0:
            farm.sponsorship_progress = min(100, int((total / goal) * 100))
        else:
            farm.sponsorship_progress = 0
        farm.total_sponsorship_amount = total
    return render(request, 'farmers/farm_list.html', {'farms': farms})
def farmer_support_list(request):
    activities = FarmerSupportActivity.objects.order_by('-date')
    return render(request, 'farmers/support_list.html', {'activities': activities})

def farmer_list(request):
    farmers = Farmer.objects.filter(user__is_active=True)
    featured_farmers = Farmer.objects.filter(is_featured=True)
    return render(request, 'farmers/list.html', {
        'farmers': farmers,
        'featured_farmers': featured_farmers,
    })

def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk, user__is_active=True)
    stories = FarmerStory.objects.filter(farmer=farmer, is_published=True)
    return render(request, 'farmers/detail.html', {
        'farmer': farmer,
        'stories': stories,
    })