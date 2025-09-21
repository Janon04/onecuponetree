from django.urls import path

app_name = 'shop'


from .views import product_list, add_to_cart, view_cart, checkout, order_success

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
]
