"""
Django management command to fix hard-coded media URLs in database content.

This command searches for and replaces hard-coded IP-based media URLs with relative paths
that work with Django's MEDIA_URL setting.

Usage:
    python manage.py fix_media_urls --dry-run  # Preview changes without applying them
    python manage.py fix_media_urls             # Apply changes to database
    python manage.py fix_media_urls --old-url "http://192.168.1.100:8000/media/"

For more information, see: ADMIN_DOCUMENTATION.md (Media Files Management section)
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
import re


class Command(BaseCommand):
    help = 'Fix hard-coded media URLs in database content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without applying them',
        )
        parser.add_argument(
            '--old-url',
            type=str,
            default='http://159.198.68.63:81/media/',
            help='The old hard-coded URL pattern to replace (default: http://159.198.68.63:81/media/)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        old_url = options['old_url']
        
        self.stdout.write(self.style.WARNING(
            f"{'[DRY RUN] ' if dry_run else ''}Searching for hard-coded URLs: {old_url}"
        ))
        
        # Pattern to match hard-coded URLs
        # Matches: http://159.198.68.63:81/media/... or similar IP-based URLs
        url_pattern = re.compile(
            r'https?://[\d\.]+(?::\d+)?/media/',
            re.IGNORECASE
        )
        
        total_changes = 0
        
        # Get all models
        all_models = apps.get_models()
        
        for model in all_models:
            model_name = f"{model._meta.app_label}.{model._meta.model_name}"
            
            # Get all text and char fields
            text_fields = []
            for field in model._meta.fields:
                if field.get_internal_type() in ['TextField', 'CharField']:
                    text_fields.append(field.name)
            
            if not text_fields:
                continue
            
            # Query all objects
            try:
                objects = model.objects.all()
                model_changes = 0
                
                for obj in objects:
                    obj_changed = False
                    
                    for field_name in text_fields:
                        field_value = getattr(obj, field_name, '')
                        
                        if field_value and isinstance(field_value, str):
                            # Check if the field contains hard-coded URLs
                            if url_pattern.search(field_value):
                                # Replace hard-coded URLs with relative paths
                                # Replace http://159.198.68.63:81/media/gallery/image.jpg with /media/gallery/image.jpg
                                new_value = url_pattern.sub('/media/', field_value)
                                
                                if new_value != field_value:
                                    self.stdout.write(
                                        self.style.SUCCESS(
                                            f"  [{model_name}] {obj.pk} - {field_name}:"
                                        )
                                    )
                                    self.stdout.write(f"    OLD: {field_value[:100]}...")
                                    self.stdout.write(f"    NEW: {new_value[:100]}...")
                                    
                                    if not dry_run:
                                        setattr(obj, field_name, new_value)
                                        obj_changed = True
                                    
                                    model_changes += 1
                    
                    if obj_changed and not dry_run:
                        obj.save()
                
                if model_changes > 0:
                    total_changes += model_changes
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {model_name}: {model_changes} field(s) updated"
                        )
                    )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Error processing {model_name}: {str(e)}"
                    )
                )
        
        if total_changes == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ No hard-coded media URLs found in database!"
                )
            )
        else:
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n[DRY RUN] Found {total_changes} field(s) with hard-coded URLs."
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        "Run without --dry-run to apply changes."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✓ Successfully updated {total_changes} field(s)!"
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "All hard-coded media URLs have been replaced with relative paths."
                    )
                )
