from django.core.management.base import BaseCommand
from farmers.models import Farmer
import random

def generate_unique_household_id(existing_ids):
    while True:
        new_id = str(random.randint(10**15, 10**16-1))
        if new_id not in existing_ids:
            return new_id

class Command(BaseCommand):
    help = 'Assigns a unique 16-digit household_id to all Farmer records with a blank or null household_id.'

    def handle(self, *args, **options):
        farmers = Farmer.objects.all()
        existing_ids = set(Farmer.objects.values_list('household_id', flat=True))
        updated = 0
        for farmer in farmers:
            if not farmer.household_id or len(farmer.household_id) != 16 or not farmer.household_id.isdigit():
                new_id = generate_unique_household_id(existing_ids)
                farmer.household_id = new_id
                farmer.save()
                existing_ids.add(new_id)
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Updated Farmer {farmer.id} with household_id {new_id}'))
        if updated == 0:
            self.stdout.write(self.style.SUCCESS('All Farmer records already have valid household_id values.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated {updated} Farmer records with new household_id values.'))
