#!/usr/bin/env python
"""
Production deployment checklist for Django project.
This script verifies your Django project is production-ready, including:
- Media files configuration
- Static files setup
- Settings validation
- Database checks for hard-coded URLs

Usage:
    python production_checklist.py
    python production_checklist.py --include-url-check  # Also scan for hard-coded URLs
"""

import os
import sys
import sqlite3
import re
from pathlib import Path


def check_file(file_path, description):
    """Check if a file exists."""
    if Path(file_path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND: {file_path}")
        return False


def check_directory(dir_path, description):
    """Check if a directory exists and is writable."""
    if Path(dir_path).exists():
        if os.access(dir_path, os.W_OK):
            print(f"✅ {description} (writable)")
            return True
        else:
            print(f"⚠️  {description} (not writable)")
            return False
    else:
        print(f"❌ {description} - NOT FOUND: {dir_path}")
        return False


def check_settings():
    """Check Django settings for media configuration."""
    print("\n📋 Checking Django Settings...")
    print("-" * 70)
    
    settings_found = False
    settings_paths = [
        'onecup_one_tree_website/settings.py',
        'settings.py',
        'config/settings.py',
    ]
    
    for settings_path in settings_paths:
        if Path(settings_path).exists():
            settings_found = True
            with open(settings_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check MEDIA_URL
                if "MEDIA_URL = '/media/'" in content or 'MEDIA_URL = "/media/"' in content:
                    print("✅ MEDIA_URL is set to '/media/'")
                else:
                    print("⚠️  MEDIA_URL might not be correctly set")
                
                # Check MEDIA_ROOT
                if "MEDIA_ROOT" in content:
                    print("✅ MEDIA_ROOT is configured")
                else:
                    print("❌ MEDIA_ROOT is not configured")
                
                # Check DEBUG
                if "DEBUG = True" in content:
                    print("⚠️  DEBUG is set to True (set to False in production!)")
                elif "DEBUG = False" in content:
                    print("✅ DEBUG is set to False (production ready)")
                
                # Check ALLOWED_HOSTS
                if "ALLOWED_HOSTS" in content and "ALLOWED_HOSTS = []" not in content:
                    print("✅ ALLOWED_HOSTS is configured")
                else:
                    print("⚠️  ALLOWED_HOSTS might not be properly configured for production")
            
            break
    
    if not settings_found:
        print("❌ Django settings.py not found")
        return False
    
    return True


def check_urls():
    """Check URLs configuration for media serving."""
    print("\n📋 Checking URLs Configuration...")
    print("-" * 70)
    
    urls_paths = [
        'onecup_one_tree_website/urls.py',
        'urls.py',
        'config/urls.py',
    ]
    
    for urls_path in urls_paths:
        if Path(urls_path).exists():
            with open(urls_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'static(settings.MEDIA_URL' in content:
                    print("✅ Media URL patterns are configured")
                else:
                    print("⚠️  Media URL patterns might not be configured")
                
                if 'if settings.DEBUG:' in content:
                    print("✅ Media serving is set for development")
                    print("   ℹ️  Remember: In production, use web server (Nginx/Apache) to serve media")
                else:
                    print("⚠️  Development media serving configuration not found")
            
            return True
    
    print("❌ Django urls.py not found")
    return False


def check_media_directory():
    """Check media directory structure."""
    print("\n📋 Checking Media Directory...")
    print("-" * 70)
    
    media_dir = Path('media')
    
    if not media_dir.exists():
        print("❌ Media directory does not exist: media/")
        print("   Create it with: mkdir media")
        return False
    
    print(f"✅ Media directory exists: {media_dir.absolute()}")
    
    # Check if writable
    if os.access(media_dir, os.W_OK):
        print("✅ Media directory is writable")
    else:
        print("⚠️  Media directory is not writable")
        print("   Fix with: chmod -R 755 media/")
        return False
    
    # Check subdirectories
    subdirs = ['gallery', 'blog', 'events', 'newsletter', 'farmer_stories']
    found_subdirs = [d.name for d in media_dir.iterdir() if d.is_dir()]
    
    if found_subdirs:
        print(f"ℹ️  Found {len(found_subdirs)} subdirectories:")
        for subdir in found_subdirs[:10]:  # Show first 10
            print(f"   • {subdir}/")
    else:
        print("ℹ️  No subdirectories found (will be created when files are uploaded)")
    
    # Count files
    all_files = list(media_dir.rglob('*.*'))
    if all_files:
        image_count = len([f for f in all_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']])
        video_count = len([f for f in all_files if f.suffix.lower() in ['.mp4', '.webm', '.mov']])
        print(f"ℹ️  Media files: {image_count} images, {video_count} videos")
    
    return True


def check_static_files():
    """Check static files configuration."""
    print("\n📋 Checking Static Files...")
    print("-" * 70)
    
    static_dir = Path('static')
    staticfiles_dir = Path('staticfiles')
    
    if static_dir.exists():
        print(f"✅ Static source directory exists: {static_dir.absolute()}")
    else:
        print("⚠️  Static directory not found: static/")
    
    if staticfiles_dir.exists():
        print(f"✅ Collected static files directory exists: {staticfiles_dir.absolute()}")
        print("   ℹ️  Static files have been collected (good for production)")
    else:
        print("⚠️  Staticfiles directory not found")
        print("   Run: python manage.py collectstatic")
    
    return True


def check_nginx_config():
    """Provide Nginx configuration example."""
    print("\n📋 Web Server Configuration (Nginx Example)")
    print("-" * 70)
    print("For production, configure your web server to serve media files:")
    print()
    print("location /media/ {")
    print("    alias /path/to/your/project/media/;")
    print("    expires 1y;")
    print("    add_header Cache-Control \"public\";")
    print("}")
    print()
    print("location /static/ {")
    print("    alias /path/to/your/project/staticfiles/;")
    print("    expires 1y;")
    print("    add_header Cache-Control \"public\";")
    print("}")


def check_requirements():
    """Check if required packages are listed."""
    print("\n📋 Checking Requirements...")
    print("-" * 70)
    
    req_files = ['requirements.txt', 'requirements_no_gdal.txt']
    found = False
    
    for req_file in req_files:
        if Path(req_file).exists():
            print(f"✅ Requirements file found: {req_file}")
            with open(req_file, 'r') as f:
                content = f.read()
                if 'Pillow' in content or 'pillow' in content:
                    print("✅ Pillow is listed (required for image handling)")
                else:
                    print("⚠️  Pillow not found in requirements")
            found = True
            break
    
    if not found:
        print("⚠️  No requirements.txt found")
    
    return True


def check_for_hardcoded_urls():
    """Check database for hard-coded media URLs."""
    print("\n📋 Checking for Hard-Coded Media URLs...")
    print("-" * 70)
    
    db_path = 'db.sqlite3'
    if not Path(db_path).exists():
        print("⚠️  Database file not found - skipping URL check")
        return True
    
    url_pattern = re.compile(r'https?://[\d\.]+(?::\d+)?/media/', re.IGNORECASE)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        total_issues = 0
        for (table_name,) in tables:
            if table_name.startswith('django_') or table_name.startswith('auth_') or table_name.startswith('sqlite_'):
                continue
            
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                text_columns = [col[1] for col in columns if col[2].upper() in ['TEXT', 'VARCHAR', 'CHAR']]
                
                if not text_columns:
                    continue
                
                for column in text_columns:
                    cursor.execute(
                        f"SELECT id FROM {table_name} WHERE {column} LIKE '%http://%/media/%' OR {column} LIKE '%https://%/media/%' LIMIT 1"
                    )
                    if cursor.fetchone():
                        total_issues += 1
                        print(f"⚠️  Found hard-coded URLs in table: {table_name}, column: {column}")
            except sqlite3.OperationalError:
                pass
        
        conn.close()
        
        if total_issues > 0:
            print(f"\n❌ Found hard-coded media URLs in {total_issues} location(s)")
            print("   Run: python check_media_urls.py for details")
            print("   Fix: python manage.py fix_media_urls")
            return False
        else:
            print("✅ No hard-coded media URLs found in database")
            return True
    
    except Exception as e:
        print(f"⚠️  Could not check database: {e}")
        return True


def main():
    """Run all checks."""
    print("=" * 70)
    print("  Django Production Checklist")
    print("=" * 70)
    
    all_passed = True
    
    # Check if detailed URL scan requested
    include_url_check = '--include-url-check' in sys.argv
    
    # Run all checks
    all_passed &= check_settings()
    all_passed &= check_urls()
    all_passed &= check_media_directory()
    all_passed &= check_static_files()
    all_passed &= check_requirements()
    
    if include_url_check:
        all_passed &= check_for_hardcoded_urls()
    else:
        print("\n💡 Tip: Run with --include-url-check to scan for hard-coded media URLs")
    
    check_nginx_config()
    
    # Final summary
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ Production Checklist Complete!")
        print("\nYour Django project appears to be properly configured.")
        print("\nFinal steps for deployment:")
        print("  1. Set DEBUG = False in settings.py")
        print("  2. Configure ALLOWED_HOSTS with your domain")
        print("  3. Set up your web server (Nginx/Apache) to serve media files")
        print("  4. Run: python manage.py collectstatic")
        print("  5. Ensure proper file permissions on media directory")
        print("  6. Consider using cloud storage (AWS S3, Azure Blob, etc.)")
        print("\nAdditional checks:")
        print("  • Run: python check_media_urls.py (detailed URL scan)")
        print("  • Run: python manage.py check --deploy (Django deployment checks)")
    else:
        print("⚠️  Some issues found - please review above")
        print("\nFor help:")
        print("  • See: ADMIN_DOCUMENTATION.md (Media Files Management section)")
        print("  • Run: python check_media_urls.py (for URL issues)")
        print("  • Run: python manage.py fix_media_urls (to fix hard-coded URLs)")
    
    print("=" * 70)


if __name__ == '__main__':
    main()
