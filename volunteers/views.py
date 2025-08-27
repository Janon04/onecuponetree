from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import VolunteerOpportunity, VolunteerApplication, BaristaTrainee
from .forms import VolunteerApplicationForm, BaristaTrainingApplicationForm

def volunteer_opportunities(request):
    opportunities = VolunteerOpportunity.objects.filter(is_active=True)
    return render(request, 'volunteers/opportunities.html', {
        'opportunities': opportunities,
    })

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(VolunteerOpportunity, pk=pk, is_active=True)
    return render(request, 'volunteers/opportunity_detail.html', {
        'opportunity': opportunity,
    })

def apply_opportunity(request, pk):
    opportunity = get_object_or_404(VolunteerOpportunity, pk=pk, is_active=True)
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.opportunity = opportunity
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            messages.success(request, _("Thank you for your application!"))
            return redirect('volunteers:opportunities')
    else:
        form = VolunteerApplicationForm()
    return render(request, 'volunteers/apply.html', {
        'form': form,
        'opportunity': opportunity,
    })

def barista_training(request):
    if request.method == 'POST':
        form = BaristaTrainingApplicationForm(request.POST)
        if form.is_valid():
            trainee = form.save(commit=False)
            if request.user.is_authenticated:
                trainee.user = request.user
            trainee.save()
            messages.success(request, _("Thank you for applying to the Barista Training Program!"))
            return redirect('volunteers:barista_training')
    else:
        form = BaristaTrainingApplicationForm()
    return render(request, 'volunteers/barista_training.html', {'form': form})