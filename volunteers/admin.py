from django.contrib import admin
from .models import VolunteerOpportunity, VolunteerApplication, BaristaTraining, BaristaTrainingApplication

admin.site.register(VolunteerOpportunity)
admin.site.register(VolunteerApplication)
admin.site.register(BaristaTraining)
admin.site.register(BaristaTrainingApplication)