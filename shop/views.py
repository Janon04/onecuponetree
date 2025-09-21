
from urllib import request
from django.shortcuts import render
from .models import Product, Cart, CartItem, Order


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .models import Order


def product_list(request):
	products = Product.objects.filter(is_active=True)
	return render(request, "shop/product_list.html", {"products": products})

# Add to cart view
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
def add_to_cart(request):
	product_id = request.POST.get("product_id")
	quantity = int(request.POST.get("quantity", 1))
	product = Product.objects.get(id=product_id)
	session_key = request.session.session_key or request.session.save() or request.session.session_key
	cart, created = Cart.objects.get_or_create(session_key=session_key)
	item, created = CartItem.objects.get_or_create(cart=cart, product=product)
	item.quantity += quantity
	item.save()
	return redirect("shop:view_cart")

# View cart
def view_cart(request):
	session_key = request.session.session_key
	cart = Cart.objects.filter(session_key=session_key).first()
	items = cart.items.all() if cart else []
	if request.method == "POST":
		for item in items:
			qty_field = f"quantity_{item.id}"
			new_qty = request.POST.get(qty_field)
			if new_qty:
				item.quantity = int(new_qty)
				item.save()
		# Refresh items after update
		items = cart.items.all() if cart else []
	total = sum(item.product.price * item.quantity for item in items)
	return render(request, "shop/cart.html", {"cart": cart, "items": items, "total": total})

# Checkout view
from django import forms
class CheckoutForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ["full_name", "email", "phone", "country", "city", "zip_code", "delivery_method"]

def checkout(request):
	session_key = request.session.session_key
	cart = Cart.objects.filter(session_key=session_key).first()
	items = cart.items.all() if cart else []
	total = sum(item.product.price * item.quantity for item in items)
	if request.method == "POST":
		form = CheckoutForm(request.POST)
		if form.is_valid() and cart:
			order = form.save(commit=False)
			order.cart = cart
			order.total_amount = total
			order.status = "pending"
			order.save()
			# Simulate payment (mock gateway)
			from .models import MockIremboPayGateway
			gateway = MockIremboPayGateway.objects.first()
			if gateway:
				gateway.process_payment(order)
			# Send email notification to admin
			from django.core.mail import send_mail
			from django.conf import settings
			# Build detailed order info for email
			order_details = [
				f"Order #{order.id}",
				f"Name: {order.full_name}",
				f"Email: {order.email}",
				f"Phone: {order.phone}",
				f"Country: {order.country}",
				f"City: {order.city}",
				f"ZIP: {order.zip_code}",
				f"Delivery Method: {order.delivery_method}",
				"\nCart Items:",
			]
			for item in items:
				order_details.append(f"- {item.product.name} ({item.quantity} x {item.product.price} {item.product.currency}) = {item.product.price * item.quantity} {item.product.currency}")
			order_details.append(f"\nTotal: {order.total_amount} RWF")
			send_mail(
				subject="New Shop Order Received",
				message="\n".join(order_details),
				from_email=settings.DEFAULT_FROM_EMAIL,
				recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
				fail_silently=True,
			)
			# Clear cart
			cart.delete()
			return redirect("shop:order_success")
	else:
		form = CheckoutForm()
	return render(request, "shop/checkout.html", {"form": form, "items": items, "total": total})

# Order success view
def order_success(request):
	return render(request, "shop/order_success.html")

