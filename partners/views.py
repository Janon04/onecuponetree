from django.views.generic import ListView
from .models import Partner

class PartnerListView(ListView):
    model = Partner
    template_name = 'partners/partner_list.html'
    context_object_name = 'partners'
    queryset = Partner.objects.filter(is_active=True)
