from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum  
from .models import ImpactStat, Testimonial
from apps.trees.models import Tree
from farmers.models import Farmer
from core.models import Donation

def impact_dashboard(request):
    from datetime import datetime
    # Get year from GET param, default to current year
    selected_year = request.GET.get('year')
    try:
        selected_year = int(selected_year)
    except (TypeError, ValueError):
        selected_year = datetime.now().year

    # Trees planted by district (all years)
    district_counts = Tree.objects.values('location').annotate(count=models.Count('id')).order_by('-count')
    district_labels = [d['location'] for d in district_counts]
    district_data = [d['count'] for d in district_counts]
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('core:home')
    from django.db.models.functions import TruncMonth
    import json

    # Use ImpactStat for all key stats, fallback to calculated if missing
    impact_stats = ImpactStat.objects.filter(is_active=True)
    stats_dict = {stat.stat_name.lower().replace(' ', '_'): stat for stat in impact_stats}
    stats = {
        'trees_planted': stats_dict.get('trees_planted', None) or Tree.objects.filter(is_active=True).count(),
        'youth_trained': stats_dict.get('youth_trained', None) or 0,
        'coffee_cups_sold': stats_dict.get('coffee_cups_sold', None) or 0,
        'farmers_supported': stats_dict.get('farmers_supported', None) or Farmer.objects.count(),
        'total_donations': stats_dict.get('total_donations', None) or Donation.objects.filter(payment_status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        'recent_donations': Donation.objects.filter(payment_status='paid').order_by('-created_at')[:5],
    }

    # Monthly trees planted
    from datetime import datetime
    from collections import OrderedDict
    import calendar
    # Get year from GET param, default to current year
    selected_year = request.GET.get('year')
    try:
        selected_year = int(selected_year)
    except (TypeError, ValueError):
        selected_year = datetime.now().year
    months = [str(m) for m in range(1, 13)]
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Trees per month (all years)
    trees_monthly = Tree.objects.extra({
        'month': "strftime('%%m', planted_date)"
    }).values('month').annotate(count=models.Count('id')).order_by('month')
    trees_month_dict = {str(int(m['month'])): m['count'] for m in trees_monthly}
    trees_month_data = [trees_month_dict.get(m, 0) for m in months]

    # Donations per month (all years)
    donations_monthly = Donation.objects.filter(payment_status='paid').extra({
        'month': "strftime('%%m', created_at)"
    }).values('month').annotate(total=models.Sum('amount')).order_by('month')
    donations_month_dict = {str(int(m['month'])): float(m['total']) for m in donations_monthly}
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
    return render(request, 'dashboard/impact.html', {
        'stats': stats,
        'recent_trees': recent_trees,
        'map_trees': map_trees,
        'testimonials': testimonials,
        'impact_stats': impact_stats,
        'recent_donations': stats['recent_donations'],
        'total_donations': stats['total_donations'],
        'total_success_stories': total_success_stories,
        'month_labels': json.dumps(month_labels),
        'trees_month_data': json.dumps(trees_month_data),
        'donations_month_data': json.dumps(donations_month_data),
        'district_labels': json.dumps(district_labels),
        'district_data': json.dumps(district_data),
        'selected_year': selected_year,
        'all_years': all_years,
    })