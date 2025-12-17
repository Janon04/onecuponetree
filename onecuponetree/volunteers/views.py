from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import VolunteerOpportunity, VolunteerApplication, BaristaTraining, BaristaTrainingApplication
from .forms import VolunteerApplicationForm, BaristaTrainingEventApplicationForm

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


# --- New Barista Training Event Views ---
def barista_training_list(request):
    trainings = BaristaTraining.objects.filter(is_active=True).order_by('-date')
    return render(request, 'volunteers/barista_training_list.html', {'trainings': trainings})

def barista_training_detail(request, pk):
    training = get_object_or_404(BaristaTraining, pk=pk, is_active=True)
    return render(request, 'volunteers/barista_training_detail.html', {'training': training})

def barista_training_apply(request, pk):
    training = get_object_or_404(BaristaTraining, pk=pk, is_active=True)
    if request.method == 'POST':
        form = BaristaTrainingEventApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.training = training
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            messages.success(request, _(f"Thank you for applying to {training.title}!"))
            return redirect('volunteers:barista_training_list')
    else:
        form = BaristaTrainingEventApplicationForm()
    return render(request, 'volunteers/barista_training_apply.html', {'form': form, 'training': training})