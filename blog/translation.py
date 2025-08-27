from modeltranslation.translator import register, TranslationOptions
from .models import BlogPost, BlogCategory

@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content',)

@register(BlogCategory)
class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
