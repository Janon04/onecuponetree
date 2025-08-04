from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductCategory, Order, OrderItem
from .forms import CheckoutForm

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, AddToCartForm, ProductFilterForm



def shop_home(request):
    categories = ProductCategory.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True)[:8]
    return render(request, 'shop/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def category_detail(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'shop/product.html', {'product': product})

def cart(request):
    # Implement cart logic here
    return render(request, 'shop/cart.html')


def checkout(request):
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process order
            return redirect('shop:order_detail', transaction_id='sample-transaction-id')
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'form': form})

def order_detail(request, transaction_id):
    order = get_object_or_404(Order, transaction_id=transaction_id)
    return render(request, 'shop/order.html', {'order': order})