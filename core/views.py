from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import ContactForm, DonationForm
from django.contrib import messages
from .utils import send_donation_thank_you
from .models import Donation

class ContactView(View):
    template_name = 'core/contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name, {'form': ContactForm(), 'success': True})
        return render(request, self.template_name, {'form': form})


class HomeView(TemplateView):
    """Homepage view with hero section and impact statistics"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mock impact statistics (in production, these would come from the database)
        context.update({
            'trees_planted': 15420,
            'youth_trained': 342,
            'coffee_cups_sold': 8750,
            'co2_saved': 2340,  # in kg
        })
        
        return context


class AboutView(TemplateView):
    """About us page with mission, vision, and story"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'mission': "To create a sustainable coffee ecosystem that empowers farmers, trains youth, and restores our environment through innovative tree planting initiatives.",
            'vision': "A world where every cup of coffee contributes to environmental restoration and economic empowerment of local communities.",
            'values': [
                {
                    'name': 'Sustainability',
                    'description': 'We prioritize environmental conservation and sustainable farming practices.'
                },
                {
                    'name': 'Education',
                    'description': 'We believe in empowering youth through comprehensive barista training and skills development.'
                },
                {
                    'name': 'Empowerment',
                    'description': 'We support coffee farmers with resources, training, and market access.'
                },
                {
                    'name': 'Innovation',
                    'description': 'We use technology and creative solutions to maximize our environmental impact.'
                }
            ]
        })
        
        return context


def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        print('POST data:', request.POST)
        if form.is_valid():
            print('Form is valid!')
            donation = form.save(commit=False)
            donation.payment_status = 'paid'  # Mark as paid for testing/demo
            donation.save()
            send_donation_thank_you(donation)
            messages.success(request, 'Thank you for your donation!')
            return redirect('core:donate')
        else:
            print('Form errors:', form.errors)
    else:
        form = DonationForm()
    return render(request, 'core/donate.html', {'form': form})

def donation_list(request):
    donations = Donation.objects.filter(payment_status='paid').order_by('-created_at')[:50]
    return render(request, 'core/donation_list.html', {'donations': donations})
