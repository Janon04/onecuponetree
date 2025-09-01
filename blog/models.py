from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from accounts.models import User

class BlogCategory(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    
    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('category'))
    from ckeditor.fields import RichTextField
    description = RichTextField(_('description'), blank=True, null=True)
    content = RichTextField(_('content'))
    featured_image = models.ImageField(_('featured image'), upload_to='blog/', null=True, blank=True)
    video = models.FileField(_('video'), upload_to='blog/videos/', null=True, blank=True, help_text=_('Upload a short video (mp4, mov, webm, max 50MB)'))
    is_published = models.BooleanField(_('is published'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

# Translation registration will be handled in translation.py