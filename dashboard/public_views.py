from django.shortcuts import render
from dashboard.views import impact_dashboard

def public_dashboard(request):
    # Reuse the same context as the admin dashboard, but filter out admin-only data if needed
    context = impact_dashboard(request).context_data if hasattr(impact_dashboard(request), 'context_data') else {}
    return render(request, 'dashboard/public_impact.html', context)
