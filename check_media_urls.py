#!/usr/bin/env python
"""
Quick diagnostic script to check for hard-coded media URLs in your Django project.
This script scans templates, static files, and database for hard-coded IP-based media URLs.

Usage:
    python check_media_urls.py

For more information, see: ADMIN_DOCUMENTATION.md (Media Files Management section)
"""

import sqlite3
import re
import sys
from pathlib import Path


def check_sqlite_database(db_path='db.sqlite3'):
    """Check SQLite database for hard-coded media URLs."""
    
    if not Path(db_path).exists():
        print(f"❌ Database file not found: {db_path}")
        print("Please run this script from your Django project root directory.")
        return False
    
    print(f"📊 Analyzing database: {db_path}\n")
    
    # Pattern to match hard-coded media URLs
    url_pattern = re.compile(r'https?://[\d\.]+(?::\d+)?/media/', re.IGNORECASE)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    total_issues = 0
    tables_with_issues = []
    
    for (table_name,) in tables:
        # Skip Django internal tables
        if table_name.startswith('django_') or table_name.startswith('auth_') or table_name.startswith('sqlite_'):
            continue
        
        try:
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            text_columns = [col[1] for col in columns if col[2].upper() in ['TEXT', 'VARCHAR', 'CHAR']]
            
            if not text_columns:
                continue
            
            # Check each text column
            table_issues = 0
            for column in text_columns:
                cursor.execute(
                    f"SELECT id, {column} FROM {table_name} WHERE {column} LIKE '%http://%/media/%' OR {column} LIKE '%https://%/media/%'"
                )
                results = cursor.fetchall()
                
                for row_id, content in results:
                    if content and url_pattern.search(str(content)):
                        matches = url_pattern.findall(str(content))
                        if table_issues == 0:
                            print(f"⚠️  Table: {table_name}")
                        
                        print(f"   └─ Row ID {row_id}, Column '{column}': Found {len(matches)} hard-coded URL(s)")
                        for match in set(matches):
                            print(f"      • {match}")
                        
                        table_issues += len(matches)
            
            if table_issues > 0:
                tables_with_issues.append((table_name, table_issues))
                total_issues += table_issues
                print()
        
        except sqlite3.OperationalError as e:
            # Skip tables that cause errors
            pass
    
    conn.close()
    
    # Summary
    print("=" * 70)
    if total_issues > 0:
        print(f"❌ Found {total_issues} hard-coded media URL(s) in {len(tables_with_issues)} table(s):\n")
        for table, count in tables_with_issues:
            print(f"   • {table}: {count} URL(s)")
        
        print("\n" + "=" * 70)
        print("🔧 To fix these issues, run one of the following:\n")
        print("   1. Django management command:")
        print("      python manage.py fix_media_urls --dry-run  # Preview")
        print("      python manage.py fix_media_urls            # Apply\n")
        print("   2. SQL script:")
        print("      sqlite3 db.sqlite3 < fix_media_urls.sql\n")
        print("   3. Manual fix:")
        print("      Open Django admin and edit the affected content")
        return False
    else:
        print("✅ No hard-coded media URLs found!")
        print("Your database content looks good.\n")
        print("If you're still experiencing 404 errors, check:")
        print("   • Web server configuration (Nginx/Apache)")
        print("   • File permissions on media directory")
        print("   • MEDIA_URL and MEDIA_ROOT settings")
        print("   • That media files actually exist on disk")
        return True


def check_templates(templates_dir='templates'):
    """Check template files for hard-coded media URLs."""
    
    if not Path(templates_dir).exists():
        print(f"⚠️  Templates directory not found: {templates_dir}")
        return True
    
    print(f"\n📄 Checking templates in: {templates_dir}\n")
    
    url_pattern = re.compile(r'https?://[\d\.]+(?::\d+)?/media/', re.IGNORECASE)
    template_files = list(Path(templates_dir).rglob('*.html'))
    
    total_issues = 0
    
    for template_path in template_files:
        try:
            content = template_path.read_text(encoding='utf-8')
            matches = url_pattern.findall(content)
            
            if matches:
                print(f"⚠️  {template_path.relative_to(templates_dir)}")
                for match in set(matches):
                    print(f"   • {match}")
                total_issues += len(matches)
        except Exception as e:
            pass
    
    if total_issues > 0:
        print(f"\n❌ Found {total_issues} hard-coded URL(s) in templates")
        print("Please update templates to use {{ object.image.url }} or {{ MEDIA_URL }}")
        return False
    else:
        print("✅ No hard-coded URLs in templates")
        return True


def check_static_files(static_dir='static'):
    """Check static files (JS/CSS) for hard-coded media URLs."""
    
    if not Path(static_dir).exists():
        print(f"⚠️  Static directory not found: {static_dir}")
        return True
    
    print(f"\n🎨 Checking static files in: {static_dir}\n")
    
    url_pattern = re.compile(r'https?://[\d\.]+(?::\d+)?/media/', re.IGNORECASE)
    static_files = list(Path(static_dir).rglob('*.js')) + list(Path(static_dir).rglob('*.css'))
    
    total_issues = 0
    
    for static_path in static_files:
        # Skip minified files
        if '.min.' in str(static_path):
            continue
        
        try:
            content = static_path.read_text(encoding='utf-8')
            matches = url_pattern.findall(content)
            
            if matches:
                print(f"⚠️  {static_path.relative_to(static_dir)}")
                for match in set(matches):
                    print(f"   • {match}")
                total_issues += len(matches)
        except Exception as e:
            pass
    
    if total_issues > 0:
        print(f"\n❌ Found {total_issues} hard-coded URL(s) in static files")
        print("Please update to use relative URLs or Django context variables")
        return False
    else:
        print("✅ No hard-coded URLs in static files")
        return True


def main():
    """Run all checks."""
    print("=" * 70)
    print("  Django Media URL Checker")
    print("  Scanning for hard-coded IP-based media URLs...")
    print("=" * 70 + "\n")
    
    db_ok = check_sqlite_database()
    templates_ok = check_templates()
    static_ok = check_static_files()
    
    print("\n" + "=" * 70)
    if db_ok and templates_ok and static_ok:
        print("✅ All checks passed!")
        print("Your project is properly configured for media URLs.")
        sys.exit(0)
    else:
        print("❌ Issues found - please review and fix")
        print("\nFor help:")
        print("  • See: ADMIN_DOCUMENTATION.md (Media Files Management section)")
        print("  • Run: python manage.py fix_media_urls (to fix database URLs)")
        print("  • Run: python production_checklist.py (deployment readiness)")
        sys.exit(1)


if __name__ == '__main__':
    main()
