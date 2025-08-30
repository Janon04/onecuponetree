from django.shortcuts import render, redirect
from django.db.models import Sum  
from .models import ImpactStat, Testimonial
from trees.models import Tree
from farmers.models import Farmer
from core.models import Donation

def impact_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('core:home')
    stats = {
        'trees_planted': Tree.objects.filter(is_active=True).count(),
        'farmers_supported': Farmer.objects.count(),
        # 'youth_trained': BaristaTrainee.objects.filter(graduated=True).count(),
        'total_donations': Donation.objects.filter(payment_status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        'recent_donations': Donation.objects.filter(payment_status='paid').order_by('-created_at')[:5],
    }
    
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
    })