from django.core.management.base import BaseCommand
from volunteers.models import Skill, Motivation, ExpectedSkill

class Command(BaseCommand):
    help = 'Populate selectable answers for BaristaTrainingApplication fields.'

    def handle(self, *args, **options):
        skills = [
            'Customer Service',
            'Teamwork',
            'Time Management',
            'Attention to Detail',
            'Adaptability',
            'Cleanliness & Hygiene',
            'Cash Handling & POS Operation',
            'Coffee Brewing',
        ]
        motivations = [
            'Career advancement',
            'Personal interest',
            'Networking',
            'Other',
            'To gain practical barista skills for employment',
            'To start my own coffee business',
            'To improve my coffee knowledge and expertise',
            'To network with industry professionals',
            'To pursue a career in hospitality',
            'To enhance my current job performance',
            'To explore new career opportunities',
            'Personal interest in coffee culture',
        ]
        expected_skills = [
            'Barista basics and techniques',
            'Coffee brewing methods',
            'Customer service skills',
            'Latte art skills',
            'Equipment maintenance',
            'Hygiene and safety practices',
            'Coffee business management',
            'Teamwork and leadership',
        ]
        for label in skills:
            Skill.objects.get_or_create(label=label)
        for label in motivations:
            Motivation.objects.get_or_create(label=label)
        for label in expected_skills:
            ExpectedSkill.objects.get_or_create(label=label)
        self.stdout.write(self.style.SUCCESS('Selectable answers populated.'))
