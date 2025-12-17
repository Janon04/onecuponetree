from django.core.management.base import BaseCommand
from get_involved.models import Motivation

SUGGESTED_ANSWERS = [
    "I want to contribute to my community",
    "I am passionate about the initiative's mission",
    "I want to gain new skills and experience",
    "I want to meet new people and network",
    "I want to support environmental activities",
    "Other",
]

class Command(BaseCommand):
    help = 'Populate Motivation model with suggested answers for join form.'

    def handle(self, *args, **options):
        created = 0
        for label in SUGGESTED_ANSWERS:
            obj, was_created = Motivation.objects.get_or_create(label=label)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'{created} motivation choices added.'))
