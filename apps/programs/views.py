from django.shortcuts import render
from .models import Program, BaristaTraining, FarmerSupport, ReusableCupCampaign

def programs(request):
    programs = Program.objects.filter(is_active=True)
    return render(request, 'programs/list.html', {'programs': programs})

def barista_academy(request):
    try:
        barista_training = BaristaTraining.objects.get(program__is_active=True)
    except BaristaTraining.DoesNotExist:
        barista_training = None
    return render(request, 'programs/barista_academy.html', {
        'barista_training': barista_training,
    })

def farmer_support(request):
    try:
        farmer_support = FarmerSupport.objects.get(program__is_active=True)
    except FarmerSupport.DoesNotExist:
        farmer_support = None
    return render(request, 'programs/farmer_support.html', {
        'farmer_support': farmer_support,
    })

def reusable_cups(request):
    try:
        cup_campaign = ReusableCupCampaign.objects.get(program__is_active=True)
    except ReusableCupCampaign.DoesNotExist:
        cup_campaign = None
    return render(request, 'programs/reusable_cups.html', {
        'cup_campaign': cup_campaign,
    })