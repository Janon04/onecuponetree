from django.shortcuts import render
from django.db.models import Sum  
from .models import ImpactStat, Testimonial
from apps.trees.models import Tree
from apps.farmers.models import Farmer
from apps.volunteers.models import BaristaTrainee
from apps.shop.models import ReusableCup

def impact_dashboard(request):
    stats = {
        'trees_planted': Tree.objects.filter(is_active=True).count(),
        'farmers_supported': Farmer.objects.count(),
        'youth_trained': BaristaTrainee.objects.filter(graduated=True).count(),
        'reusable_cups': ReusableCup.objects.filter(is_active=True).count(),
        'co2_offset': Tree.objects.aggregate(total=Sum('co2_offset'))['total'] or 0,  # Now Sum is defined
    }
    
    recent_trees = Tree.objects.order_by('-planted_date')[:5]
    testimonials = Testimonial.objects.filter(is_featured=True)
    impact_stats = ImpactStat.objects.filter(is_active=True)
    
    return render(request, 'dashboard/impact.html', {
        'stats': stats,
        'recent_trees': recent_trees,
        'testimonials': testimonials,
        'impact_stats': impact_stats,
    })