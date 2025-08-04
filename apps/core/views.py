from django.shortcuts import render
from .models import SiteSetting

def home(request):
    return render(request, 'core/home.html')

def about(request):
    site_settings = SiteSetting.load()
    return render(request, 'core/about.html', {'site_settings': site_settings})

def contact(request):
    site_settings = SiteSetting.load()
    return render(request, 'core/contact.html', {'site_settings': site_settings})