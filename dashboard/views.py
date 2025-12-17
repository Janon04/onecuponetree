from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import models
from django.db.models import Sum  
from .models import ImpactStat, Testimonial
from apps.trees.models import Tree
from farmers.models import Farmer
from core.models import Donation

def impact_dashboard(request):
    """
    Backend-only dashboard view that provides data processing without frontend rendering.
    
    Functionality:
    - Calculates impact statistics (trees planted, donations, farmers supported, etc.)
    - Processes monthly chart data for trees and donations
    - Generates district-wise tree planting data
    - Supports year filtering
    
    Access:
    - Default: Redirects to home page (no frontend)
    - API: Add ?format=json to get JSON response with all data
    
    Authentication: Requires staff user authentication
    
    Returns:
    - Redirect to home page (default)
    - JSON response (when ?format=json parameter is provided)
    """
    from datetime import datetime
    
    # Check authentication - redirect if not staff
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('core:home')
    
    # Get year from GET param, default to current year
    selected_year = request.GET.get('year')
    try:
        selected_year = int(selected_year)
    except (TypeError, ValueError):
        selected_year = datetime.now().year

    # Trees planted by district (all years, limited to top 10)
    district_counts = Tree.objects.values('location').annotate(
        count=models.Count('id')
    ).exclude(location__isnull=True).exclude(location__exact='').order_by('-count')[:10]
    
    district_labels = [d['location'] for d in district_counts]
    district_data = [d['count'] for d in district_counts]
    
    # Backend authentication check moved up
    from django.db.models.functions import TruncMonth
    import json

    # Use ImpactStat for all key stats, fallback to calculated if missing
    impact_stats = ImpactStat.objects.filter(is_active=True)
    stats_dict = {stat.stat_name.lower().replace(' ', '_'): stat for stat in impact_stats}
    
    # Trees Planted
    if 'trees_planted' in stats_dict:
        trees_planted = stats_dict['trees_planted'].stat_value
    else:
        trees_planted = Tree.objects.filter(is_active=True).count()
    
    # Youth Trained
    if 'youth_trained' in stats_dict:
        youth_trained = stats_dict['youth_trained'].stat_value
    else:
        youth_trained = 0
    
    # Coffee Cups Sold
    if 'coffee_cups_sold' in stats_dict:
        coffee_cups_sold = stats_dict['coffee_cups_sold'].stat_value
    else:
        coffee_cups_sold = 0
    
    # Farmers Supported
    if 'farmers_supported' in stats_dict:
        farmers_supported = stats_dict['farmers_supported'].stat_value
    else:
        farmers_supported = Farmer.objects.count()
    
    # Total Donations
    if 'total_donations' in stats_dict:
        total_donations = stats_dict['total_donations'].stat_value
    else:
        total_donations = Donation.objects.filter(payment_status='paid').aggregate(total=Sum('amount'))['total'] or 0
    
    stats = {
        'trees_planted': trees_planted,
        'youth_trained': youth_trained,
        'coffee_cups_sold': coffee_cups_sold,
        'farmers_supported': farmers_supported,
        'total_donations': total_donations,
        'recent_donations': Donation.objects.filter(payment_status='paid').order_by('-created_at')[:5],
    }

    # Monthly trees planted
    from datetime import datetime
    from collections import OrderedDict
    import calendar
    months = [str(m) for m in range(1, 13)]
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Trees per month (current year or selected year)
    trees_monthly = Tree.objects.filter(
        planted_date__year=selected_year
    ).extra({
        'month': "strftime('%%m', planted_date)"
    }).values('month').annotate(count=models.Count('id')).order_by('month')
    
    trees_month_dict = {str(int(m['month'])): m['count'] for m in trees_monthly}
    trees_month_data = [trees_month_dict.get(m, 0) for m in months]

    # Donations per month (current year or selected year)
    donations_monthly = Donation.objects.filter(
        payment_status='paid',
        created_at__year=selected_year
    ).extra({
        'month': "strftime('%%m', created_at)"
    }).values('month').annotate(total=models.Sum('amount')).order_by('month')
    
    donations_month_dict = {str(int(m['month'])): float(m['total']) if m['total'] else 0 for m in donations_monthly}
    donations_month_data = [donations_month_dict.get(m, 0) for m in months]

    # Get all years with data for dropdown
    tree_years = Tree.objects.dates('planted_date', 'year').distinct()
    donation_years = Donation.objects.filter(payment_status='paid').dates('created_at', 'year').distinct()
    all_years = sorted(set([y.year for y in tree_years] + [y.year for y in donation_years]), reverse=True)

    recent_trees = Tree.objects.filter(latitude__isnull=False, longitude__isnull=False).order_by('-planted_date')
    # Show ALL trees with coordinates on the map
    all_trees = Tree.objects.filter(latitude__isnull=False, longitude__isnull=False)
    map_trees = [
        {
            'tree_id': t.tree_id,
            'species': t.get_species_display(),
            'planted_date': t.planted_date,
            'latitude': float(t.latitude),
            'longitude': float(t.longitude),
        }
        for t in all_trees
    ]
    testimonials = Testimonial.objects.filter(is_featured=True)
    # Farmer stories count for success stories card
    from farmers.models import FarmerStory
    total_success_stories = FarmerStory.objects.filter(is_published=True).count()
    
    # Return JSON response for API usage instead of rendering template
    if request.GET.get('format') == 'json':
        return JsonResponse({
            'stats': {
                'trees_planted': stats['trees_planted'],
                'youth_trained': stats['youth_trained'],
                'coffee_cups_sold': stats['coffee_cups_sold'],
                'farmers_supported': stats['farmers_supported'],
                'total_donations': float(stats['total_donations']),
                'total_success_stories': total_success_stories,
            },
            'charts': {
                'month_labels': month_labels,
                'trees_month_data': trees_month_data,
                'donations_month_data': donations_month_data,
                'district_labels': district_labels,
                'district_data': district_data,
            },
            'map_trees': map_trees,
            'selected_year': selected_year,
            'all_years': all_years,
        })
    
    # Redirect to home page since we removed frontend
    return redirect('core:home')