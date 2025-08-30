from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum  
from .models import ImpactStat, Testimonial
from trees.models import Tree
from farmers.models import Farmer
from core.models import Donation

def impact_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('core:home')
    from django.db.models.functions import TruncMonth
    import json

    stats = {
        'trees_planted': Tree.objects.filter(is_active=True).count(),
        'farmers_supported': Farmer.objects.count(),
        # 'youth_trained': BaristaTrainee.objects.filter(graduated=True).count(),
        'total_donations': Donation.objects.filter(payment_status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        'recent_donations': Donation.objects.filter(payment_status='paid').order_by('-created_at')[:5],
    }

    # Monthly trees planted
    from datetime import datetime
    from collections import OrderedDict
    this_year = datetime.now().year
    months = [f"{m:02d}" for m in range(1, 13)]
    month_labels = [datetime(2000, m, 1).strftime('%b') for m in range(1, 13)]
    trees_monthly = Tree.objects.filter(planted_date__year=this_year).extra({
        'month': "strftime('%%m', planted_date)"
    }).values('month').annotate(count=models.Count('id')).order_by('month')
    trees_month_dict = {m['month']: m['count'] for m in trees_monthly}
    trees_month_data = [trees_month_dict.get(m, 0) for m in months]

    # Monthly donations
    donations_monthly = Donation.objects.filter(payment_status='paid', created_at__year=this_year).extra({
        'month': "strftime('%%m', created_at)"
    }).values('month').annotate(total=models.Sum('amount')).order_by('month')
    donations_month_dict = {m['month']: float(m['total']) for m in donations_monthly}
    donations_month_data = [donations_month_dict.get(m, 0) for m in months]

    recent_trees = Tree.objects.filter(latitude__isnull=False, longitude__isnull=False).order_by('-planted_date')[:5]
    # Prepare tree data for map (id, species, planted_date, lat, lon)
    map_trees = [
        {
            'tree_id': t.tree_id,
            'species': t.get_species_display(),
            'planted_date': t.planted_date,
            'latitude': float(t.latitude),
            'longitude': float(t.longitude),
        }
        for t in recent_trees
    ]
    testimonials = Testimonial.objects.filter(is_featured=True)
    impact_stats = ImpactStat.objects.filter(is_active=True)

    return render(request, 'dashboard/impact.html', {
        'stats': stats,
        'recent_trees': recent_trees,
        'map_trees': map_trees,
        'testimonials': testimonials,
        'impact_stats': impact_stats,
        'recent_donations': stats['recent_donations'],
        'total_donations': stats['total_donations'],
        'month_labels': json.dumps(month_labels),
        'trees_month_data': json.dumps(trees_month_data),
        'donations_month_data': json.dumps(donations_month_data),
    })