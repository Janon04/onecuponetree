from newsletter.models import NewsletterSubscriber
from researchhub.models import ResearchSubscriber
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import ContactForm, DonationForm
from django.contrib import messages
from .utils import send_donation_thank_you
from .models import Donation

def unified_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        # Newsletter
        newsletter_created = False
        if not NewsletterSubscriber.objects.filter(email__iexact=email).exists():
            NewsletterSubscriber.objects.create(email=email)
            newsletter_created = True
        # Research
        research_created = False
        if not ResearchSubscriber.objects.filter(email__iexact=email).exists():
            ResearchSubscriber.objects.create(email=email)
            research_created = True
        if newsletter_created or research_created:
            messages.success(request, "Thank you for subscribing! You'll receive updates from both our Newsletter and Research & Publications.")
        else:
            messages.info(request, "You are already subscribed to both our Newsletter and Research & Publications updates.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
class ContactView(View):
    template_name = 'core/contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send notification email
            from django.core.mail import send_mail
            from django.conf import settings
            subject = f"New Contact Message: {contact.subject}"
            message = f"From: {contact.name} <{contact.email}>\n\nMessage:\n{contact.message}"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_NOTIFICATION_EMAIL]
            )
            return render(request, self.template_name, {'form': ContactForm(), 'success': True})
        return render(request, self.template_name, {'form': form})


class HomeView(TemplateView):
    """Homepage view with hero section and impact statistics"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from dashboard.models import ImpactStat
        from farmers.models import Farmer
        from apps.trees.models import Tree
        
        # Try to get stats from ImpactStat, fallback to model counts
        impact_stats = ImpactStat.objects.filter(is_active=True)
        stats_dict = {stat.stat_name.lower().replace(' ', '_'): stat for stat in impact_stats}
        
        # Trees Planted
        if 'trees_planted' in stats_dict:
            context['trees_planted'] = stats_dict['trees_planted'].stat_value
        else:
            context['trees_planted'] = Tree.objects.filter(is_active=True).count()
        
        # Youth Trained
        if 'youth_trained' in stats_dict:
            context['youth_trained'] = stats_dict['youth_trained'].stat_value
        else:
            try:
                from volunteers.models import BaristaTrainingApplication
                context['youth_trained'] = BaristaTrainingApplication.objects.filter(selected_for_training=True).count()
            except Exception:
                context['youth_trained'] = 0
        
        # Coffee Cups Sold
        if 'coffee_cups_sold' in stats_dict:
            context['coffee_cups_sold'] = stats_dict['coffee_cups_sold'].stat_value
        else:
            try:
                from shop.models import Order, CartItem
                paid_orders = Order.objects.filter(status__in=["paid", "confirmed"])
                cups_sold = 0
                for order in paid_orders:
                    if order.cart:
                        cups_sold += sum(item.quantity for item in order.cart.items.all())
                context['coffee_cups_sold'] = cups_sold
            except Exception:
                context['coffee_cups_sold'] = 0
        
        # CO2 Saved
        if 'co2_saved' in stats_dict:
            context['co2_saved'] = stats_dict['co2_saved'].stat_value
        else:
            context['co2_saved'] = 0
            
        return context


class AboutView(TemplateView):
    """About us page with mission, vision, and story"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from dashboard.models import ImpactStat
        from farmers.models import Farmer
        from apps.trees.models import Tree
        from .models import TeamMember
        
        # Try to get stats from ImpactStat, fallback to model counts
        impact_stats = ImpactStat.objects.filter(is_active=True)
        stats_dict = {stat.stat_name.lower().replace(' ', '_'): stat for stat in impact_stats}
        
        # Trees Planted
        if 'trees_planted' in stats_dict:
            context['trees_planted'] = stats_dict['trees_planted'].stat_value
        else:
            context['trees_planted'] = Tree.objects.filter(is_active=True).count()
        
        # Farmers Supported
        if 'farmers_supported' in stats_dict:
            context['farmers_supported'] = stats_dict['farmers_supported'].stat_value
        else:
            context['farmers_supported'] = Farmer.objects.count()
        
        # Youth Trained
        if 'youth_trained' in stats_dict:
            context['youth_trained'] = stats_dict['youth_trained'].stat_value
        else:
            try:
                from volunteers.models import BaristaTrainingApplication
                context['youth_trained'] = BaristaTrainingApplication.objects.filter(selected_for_training=True).count()
            except Exception:
                context['youth_trained'] = 0
        
        # Communities
        if 'communities' in stats_dict:
            context['communities'] = stats_dict['communities'].stat_value
        else:
            unique_sectors = Farmer.objects.values_list('sector', flat=True).distinct()
            context['communities'] = unique_sectors.count()
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
            ],
            'team_members': TeamMember.objects.all()
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
            # Send admin notification email
            from django.core.mail import send_mail
            from django.conf import settings
            subject = f"New Donation Received: {donation.donor_name or 'Anonymous'}"
            message = f"Amount: {donation.amount} {donation.currency}\nDonor: {donation.donor_name} <{donation.donor_email}>\nType: {donation.donation_type}\nMessage: {donation.message}"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_NOTIFICATION_EMAIL]
            )
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
