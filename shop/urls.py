from django.urls import path

app_name = 'shop'


from .views import (
    product_list, product_detail, add_to_cart, view_cart, 
    checkout, order_success, add_to_wishlist, remove_from_wishlist, 
    view_wishlist
)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    
    # Wishlist URLs
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
