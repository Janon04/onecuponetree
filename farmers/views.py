def story_list(request):
    stories = FarmerStory.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'farmers/story_list.html', {'stories': stories})
def support_activities_public(request):
    activities = FarmerSupportActivity.objects.filter(is_public=True).order_by('-date')
    return render(request, 'farmers/support_activities_public.html', {'activities': activities})
from django.shortcuts import render, get_object_or_404
from .models import Farmer, FarmerStory, FarmerSupportActivity
def farmer_support_list(request):
    activities = FarmerSupportActivity.objects.order_by('-date')
    return render(request, 'farmers/support_list.html', {'activities': activities})

def farmer_list(request):
    farmers = Farmer.objects.filter(user__is_active=True)
    featured_farmers = Farmer.objects.filter(is_featured=True)
    return render(request, 'farmers/list.html', {
        'farmers': farmers,
        'featured_farmers': featured_farmers,
    })

def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk, user__is_active=True)
    stories = FarmerStory.objects.filter(farmer=farmer, is_published=True)
    return render(request, 'farmers/detail.html', {
        'farmer': farmer,
        'stories': stories,
    })