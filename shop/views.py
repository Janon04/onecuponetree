
from urllib import request
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Product, ProductCategory, Cart, CartItem, Order



from django.http import HttpResponseRedirect
from .models import Order


def product_list(request):
	"""
	Enhanced product list view with filtering, sorting, and pagination
	"""
	# Get all active products
	products = Product.objects.filter(is_active=True).select_related('category')
	
	# Get all categories (product_count is a property on the model)
	categories = ProductCategory.objects.filter(is_active=True)
	
	# Category filtering
	active_category = request.GET.get('category')
	if active_category:
		products = products.filter(category__slug=active_category)
	
	# Search functionality
	search_query = request.GET.get('q', '').strip()
	if search_query:
		products = products.filter(
			Q(name__icontains=search_query) | 
			Q(description__icontains=search_query)
		)
	
	# Sorting
	sort_by = request.GET.get('sort', '-created_at')
	valid_sort_options = ['name', '-name', 'price', '-price', '-created_at', 'created_at']
	if sort_by in valid_sort_options:
		products = products.order_by(sort_by)
	else:
		products = products.order_by('-created_at')
	
	# Get total count before pagination
	total_products = products.count()
	
	# Pagination
	page = request.GET.get('page', 1)
	paginator = Paginator(products, 9)  # 9 products per page (3x3 grid)
	
	try:
		products_page = paginator.page(page)
	except PageNotAnInteger:
		products_page = paginator.page(1)
	except EmptyPage:
		products_page = paginator.page(paginator.num_pages)
	
	# Get cart count for header
	cart_count = 0
	session_key = request.session.session_key
	if session_key:
		cart = Cart.objects.filter(session_key=session_key).first()
		if cart:
			cart_count = sum(item.quantity for item in cart.items.all())
	
	# Get featured categories (top 3 with products)
	featured_categories = [cat for cat in categories if cat.product_count > 0][:3]
	
	# Build context
	context = {
		'products': products_page,
		'page_obj': products_page,
		'is_paginated': products_page.has_other_pages(),
		'categories': categories,
		'active_category': active_category,
		'sort_by': sort_by,
		'search_query': search_query,
		'total_products': total_products,
		'cart_count': cart_count,
		'featured_categories': featured_categories,
	}
	
	return render(request, "shop/product_list.html", context)

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

class PaymentForm(forms.Form):
	payment_method = forms.ChoiceField(
		choices=[
			('card', 'Credit/Debit Card'),
			('mobile', 'Mobile Money'),
			('bank', 'Bank Transfer')
		],
		initial='card',
		widget=forms.RadioSelect
	)
	
	# Card payment fields
	card_number = forms.CharField(max_length=19, required=False)
	card_name = forms.CharField(max_length=100, required=False)
	card_expiry = forms.CharField(max_length=5, required=False)
	card_cvv = forms.CharField(max_length=4, required=False)
	
	# Mobile money fields
	mobile_provider = forms.ChoiceField(
		choices=[
			('', 'Select Provider'),
			('mtn', 'MTN Mobile Money'),
			('airtel', 'Airtel Money')
		],
		required=False
	)
	mobile_number = forms.CharField(max_length=15, required=False)
	
	def clean(self):
		cleaned_data = super().clean()
		payment_method = cleaned_data.get('payment_method')
		
		if payment_method == 'card':
			# Validate card fields
			if not cleaned_data.get('card_number'):
				raise forms.ValidationError('Card number is required for card payments.')
			if not cleaned_data.get('card_name'):
				raise forms.ValidationError('Cardholder name is required for card payments.')
			if not cleaned_data.get('card_expiry'):
				raise forms.ValidationError('Card expiry date is required for card payments.')
			if not cleaned_data.get('card_cvv'):
				raise forms.ValidationError('CVV is required for card payments.')
				
		elif payment_method == 'mobile':
			# Validate mobile money fields
			if not cleaned_data.get('mobile_provider'):
				raise forms.ValidationError('Mobile money provider is required.')
			if not cleaned_data.get('mobile_number'):
				raise forms.ValidationError('Phone number is required for mobile money payments.')
				
		return cleaned_data

def process_payment(order, payment_data):
	"""
	Process payment based on the selected payment method
	Returns True if payment is successful, False otherwise
	"""
	payment_method = payment_data['payment_method']
	
	try:
		if payment_method == 'card':
			# Process card payment
			return process_card_payment(order, payment_data)
		elif payment_method == 'mobile':
			
			return process_mobile_payment(order, payment_data)
		elif payment_method == 'bank':
			
			return True
	except Exception as e:
		
		print(f"Payment processing error: {e}")
		return False
	
	return False

def process_card_payment(order, payment_data):
	"""
	Process credit/debit card payment
	In production, integrate with actual payment gateway like Stripe, PayPal, etc.
	"""
	# Mock card payment processing
	card_number = payment_data.get('card_number', '').replace(' ', '')
	card_name = payment_data.get('card_name')
	card_expiry = payment_data.get('card_expiry')
	card_cvv = payment_data.get('card_cvv')
	
	# Basic validation (in production, use proper payment gateway validation)
	if len(card_number) < 13 or len(card_number) > 19:
		return False
	
	if len(card_cvv) < 3 or len(card_cvv) > 4:
		return False
	
	# Simulate payment gateway response
	# In production, call actual payment gateway API
	try:
		from .models import MockIremboPayGateway
		gateway = MockIremboPayGateway.objects.first()
		if gateway:
			return gateway.process_payment(order)
	except:
		pass
	
	# Mock successful payment for demonstration
	return True

def process_mobile_payment(order, payment_data):
	"""
	Process mobile money payment (MTN, Airtel)
	In production, integrate with mobile money APIs
	"""
	provider = payment_data.get('mobile_provider')
	phone_number = payment_data.get('mobile_number')
	
	if not provider or not phone_number:
		return False
	
	# Clean phone number
	phone_number = phone_number.replace(' ', '').replace('-', '')
	
	# Basic phone number validation for Rwanda
	if not phone_number.startswith('+250') and not phone_number.startswith('250'):
		if phone_number.startswith('07') or phone_number.startswith('78') or phone_number.startswith('79'):
			phone_number = '+250' + phone_number[1:]
		else:
			return False
	
	# Mock mobile money processing
	if provider == 'mtn':
		# In production, integrate with MTN Mobile Money API
		return mock_mtn_payment(order, phone_number)
	elif provider == 'airtel':
		# In production, integrate with Airtel Money API
		return mock_airtel_payment(order, phone_number)
	
	return False

def mock_mtn_payment(order, phone_number):
	"""Mock MTN Mobile Money payment processing"""
	# Simulate API call to MTN
	# In production, use actual MTN Mobile Money API
	return True

def mock_airtel_payment(order, phone_number):
	"""Mock Airtel Money payment processing"""
	# Simulate API call to Airtel
	# In production, use actual Airtel Money API
	return True

def checkout(request):
	session_key = request.session.session_key
	cart = Cart.objects.filter(session_key=session_key).first()
	items = cart.items.all() if cart else []
	total = sum(item.product.price * item.quantity for item in items)
	if request.method == "POST":
		form = CheckoutForm(request.POST)
		payment_form = PaymentForm(request.POST)
		
		if form.is_valid() and payment_form.is_valid() and cart:
			order = form.save(commit=False)
			order.cart = cart
			order.total_amount = total
			order.status = "pending"
			order.save()
			
			# Process payment based on selected method
			payment_method = payment_form.cleaned_data['payment_method']
			payment_success = process_payment(order, payment_form.cleaned_data)
			
			if payment_success:
				order.status = "confirmed" if payment_method != 'bank' else "pending_bank_transfer"
				order.save()
			# Send email notification to admin
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
			order_details.append(f"Payment Method: {payment_method.upper()}")
			
			# Add payment details based on method
			if payment_method == 'card':
				card_last4 = payment_form.cleaned_data.get('card_number', '')[-4:] if payment_form.cleaned_data.get('card_number') else 'N/A'
				order_details.append(f"Card ending in: ****{card_last4}")
			elif payment_method == 'mobile':
				provider = payment_form.cleaned_data.get('mobile_provider', 'N/A')
				phone = payment_form.cleaned_data.get('mobile_number', 'N/A')
				order_details.append(f"Mobile Provider: {provider}")
				order_details.append(f"Phone Number: {phone}")
			
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
			# Payment failed
			return render(request, "shop/checkout.html", {
				"form": form, 
				"payment_form": payment_form,
				"items": items, 
				"total": total,
				"payment_error": "Payment processing failed. Please try again."
			})
	else:
		form = CheckoutForm()
		payment_form = PaymentForm()
	
	return render(request, "shop/checkout.html", {
		"form": form, 
		"payment_form": payment_form,
		"items": items, 
		"total": total
	})

# Order success view
def order_success(request):
	return render(request, "shop/order_success.html")


# Product detail view
def product_detail(request, slug):
	"""
	Product detail page with reviews
	"""
	from django.shortcuts import get_object_or_404
	from .models import ProductReview
	
	product = get_object_or_404(Product, slug=slug, is_active=True)
	
	# Get approved reviews
	reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
	
	# Get related products (same category)
	related_products = Product.objects.filter(
		category=product.category,
		is_active=True
	).exclude(id=product.id)[:4]
	
	# Get cart count
	cart_count = 0
	session_key = request.session.session_key
	if session_key:
		cart = Cart.objects.filter(session_key=session_key).first()
		if cart:
			cart_count = sum(item.quantity for item in cart.items.all())
	
	context = {
		'product': product,
		'reviews': reviews,
		'related_products': related_products,
		'cart_count': cart_count,
	}
	
	return render(request, "shop/product_detail.html", context)


# Wishlist views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Wishlist


@login_required
@require_POST
def add_to_wishlist(request, product_id):
	"""
	Add a product to the user's wishlist
	"""
	try:
		product = Product.objects.get(id=product_id, is_active=True)
		wishlist_item, created = Wishlist.objects.get_or_create(
			user=request.user,
			product=product
		)
		
		if created:
			return JsonResponse({
				'success': True,
				'message': 'Added to wishlist!',
				'in_wishlist': True
			})
		else:
			return JsonResponse({
				'success': True,
				'message': 'Already in wishlist',
				'in_wishlist': True
			})
	except Product.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'Product not found'
		}, status=404)
	except Exception as e:
		return JsonResponse({
			'success': False,
			'message': 'Error adding to wishlist'
		}, status=500)


@login_required
@require_POST
def remove_from_wishlist(request, product_id):
	"""
	Remove a product from the user's wishlist
	"""
	try:
		wishlist_item = Wishlist.objects.get(
			user=request.user,
			product_id=product_id
		)
		wishlist_item.delete()
		
		return JsonResponse({
			'success': True,
			'message': 'Removed from wishlist',
			'in_wishlist': False
		})
	except Wishlist.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'Item not in wishlist'
		}, status=404)
	except Exception as e:
		return JsonResponse({
			'success': False,
			'message': 'Error removing from wishlist'
		}, status=500)


@login_required
def view_wishlist(request):
	"""
	Display the user's wishlist
	"""
	wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
	
	# Get cart count for navbar
	cart_count = 0
	session_key = request.session.session_key
	if session_key:
		cart = Cart.objects.filter(session_key=session_key).first()
		if cart:
			cart_count = sum(item.quantity for item in cart.items.all())
	
	context = {
		'wishlist_items': wishlist_items,
		'cart_count': cart_count,
	}
	
	return render(request, 'shop/wishlist.html', context)

