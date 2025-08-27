from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog/detail.html', {'post': post})