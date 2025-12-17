from django.views.generic import ListView
from .models import GalleryImage

class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'images'
    paginate_by = 12
