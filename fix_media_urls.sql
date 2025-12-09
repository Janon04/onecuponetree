-- SQL Script to Fix Hard-Coded Media URLs in Django Database
-- This script replaces hard-coded IP-based media URLs with relative paths
-- 
-- PREFERRED METHOD: Use the Django management command instead:
--   python manage.py fix_media_urls --dry-run  # Preview changes
--   python manage.py fix_media_urls            # Apply fixes
--
-- IMPORTANT: 
-- 1. Backup your database before running this script!
-- 2. Review the affected tables and columns before executing
-- 3. Adjust the old URL pattern if your hard-coded URL is different
--
-- Usage (for SQLite):
--   sqlite3 db.sqlite3 < fix_media_urls.sql
--
-- Usage (for PostgreSQL):
--   psql -d your_database_name -f fix_media_urls.sql
--
-- For more information, see: ADMIN_DOCUMENTATION.md (Media Files Management section)

-- ==============================================================================
-- Configuration
-- ==============================================================================
-- Change this to match your hard-coded URL pattern
-- Default: 'http://159.198.68.63:81/media/'
-- Will be replaced with: '/media/'

-- ==============================================================================
-- Preview Changes (SELECT queries - safe to run)
-- ==============================================================================

-- Check Blog Posts
SELECT 
    id, 
    title, 
    content 
FROM blog_blogpost 
WHERE content LIKE '%http://%/media/%'
ORDER BY id;

-- Check Events
SELECT 
    id, 
    title, 
    description 
FROM events_event 
WHERE description LIKE '%http://%/media/%'
ORDER BY id;

-- Check Gallery Images
SELECT 
    id, 
    title, 
    description 
FROM gallery_galleryimage 
WHERE description LIKE '%http://%/media/%'
ORDER BY id;

-- Check Newsletter Content
SELECT 
    id, 
    subject, 
    content 
FROM newsletter_newsletter 
WHERE content LIKE '%http://%/media/%'
ORDER BY id;

-- Check Programs
SELECT 
    id, 
    title, 
    description 
FROM programs_program 
WHERE description LIKE '%http://%/media/%'
ORDER BY id;

-- Check Farmer Stories
SELECT 
    id, 
    title, 
    story 
FROM farmers_farmerstory 
WHERE story LIKE '%http://%/media/%'
ORDER BY id;

-- Check Volunteer Opportunities
SELECT 
    id, 
    title, 
    description 
FROM volunteers_opportunity 
WHERE description LIKE '%http://%/media/%'
ORDER BY id;

-- ==============================================================================
-- Apply Changes (UPDATE queries - will modify database)
-- ==============================================================================
-- UNCOMMENT BELOW TO EXECUTE THE FIXES
-- Make sure to backup your database first!

-- Fix Blog Posts
-- UPDATE blog_blogpost 
-- SET content = REPLACE(content, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE content LIKE '%http://159.198.68.63:81/media/%';

-- Fix Events
-- UPDATE events_event 
-- SET description = REPLACE(description, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE description LIKE '%http://159.198.68.63:81/media/%';

-- Fix Gallery Images
-- UPDATE gallery_galleryimage 
-- SET description = REPLACE(description, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE description LIKE '%http://159.198.68.63:81/media/%';

-- Fix Newsletter Content
-- UPDATE newsletter_newsletter 
-- SET content = REPLACE(content, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE content LIKE '%http://159.198.68.63:81/media/%';

-- Fix Programs
-- UPDATE programs_program 
-- SET description = REPLACE(description, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE description LIKE '%http://159.198.68.63:81/media/%';

-- Fix Farmer Stories
-- UPDATE farmers_farmerstory 
-- SET story = REPLACE(story, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE story LIKE '%http://159.198.68.63:81/media/%';

-- Fix Volunteer Opportunities
-- UPDATE volunteers_opportunity 
-- SET description = REPLACE(description, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE description LIKE '%http://159.198.68.63:81/media/%';

-- ==============================================================================
-- Generic Pattern for Other Tables
-- ==============================================================================
-- If you find hard-coded URLs in other tables, use this pattern:
--
-- UPDATE table_name 
-- SET column_name = REPLACE(column_name, 'http://159.198.68.63:81/media/', '/media/')
-- WHERE column_name LIKE '%http://159.198.68.63:81/media/%';
--
-- You can also use wildcards to match any IP address:
-- For SQLite (limited regex support):
--   Use REPLACE() multiple times if you have different IP addresses
--
-- For PostgreSQL (with regex support):
--   UPDATE table_name 
--   SET column_name = REGEXP_REPLACE(column_name, 'https?://[\d\.]+(?::\d+)?/media/', '/media/', 'g')
--   WHERE column_name ~ 'https?://[\d\.]+(?::\d+)?/media/';

-- ==============================================================================
-- Verify Changes
-- ==============================================================================
-- After running updates, verify no hard-coded URLs remain:

-- SELECT 
--     'blog_blogpost' as table_name, 
--     COUNT(*) as count 
-- FROM blog_blogpost 
-- WHERE content LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'events_event', 
--     COUNT(*) 
-- FROM events_event 
-- WHERE description LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'gallery_galleryimage', 
--     COUNT(*) 
-- FROM gallery_galleryimage 
-- WHERE description LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'newsletter_newsletter', 
--     COUNT(*) 
-- FROM newsletter_newsletter 
-- WHERE content LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'programs_program', 
--     COUNT(*) 
-- FROM programs_program 
-- WHERE description LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'farmers_farmerstory', 
--     COUNT(*) 
-- FROM farmers_farmerstory 
-- WHERE story LIKE '%http://%/media/%'
-- UNION ALL
-- SELECT 
--     'volunteers_opportunity', 
--     COUNT(*) 
-- FROM volunteers_opportunity 
-- WHERE description LIKE '%http://%/media/%';
