
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.conf import settings

# Product Category model
class ProductCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True, blank=True)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon name (e.g., 'coffee', 'leaf')")
	is_active = models.BooleanField(default=True)
	ordering = models.IntegerField(default=0, help_text="Lower numbers appear first")
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name = "Product Category"
		verbose_name_plural = "Product Categories"
		ordering = ['ordering', 'name']
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	
	def __str__(self):
		return self.name
	
	@property
	def product_count(self):
		return self.products.filter(is_active=True).count()

# Product model for shop
class Product(models.Model):
	CURRENCY_CHOICES = [
		("RWF", "Rwandan Franc"),
		("USD", "US Dollar"),
		("EUR", "Euro"),
		("KES", "Kenyan Shilling"),
		("UGX", "Ugandan Shilling"),
	]
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price for showing discounts")
	currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="RWF")
	stock_quantity = models.IntegerField(null=True, blank=True, help_text="Available stock quantity (leave empty if not tracking)")
	show_stock_publicly = models.BooleanField(default=False, help_text="Display stock quantity on public product pages")
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False, help_text="Display as featured product")
	is_new = models.BooleanField(default=False, help_text="Mark as new product")
	image = models.ImageField(upload_to="product_images/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name
	
	@property
	def average_rating(self):
		avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
		return round(avg, 1) if avg else None
	
	@property
	def review_count(self):
		return self.reviews.count()
	
	@property
	def is_in_stock(self):
		return self.stock_quantity > 0
	
	@property
	def discount_percentage(self):
		if self.compare_price and self.compare_price > self.price:
			return int(((self.compare_price - self.price) / self.compare_price) * 100)
		return 0


# Product Review model
class ProductReview(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	customer_name = models.CharField(max_length=100)
	customer_email = models.EmailField()
	rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], help_text="Rating from 1 to 5")
	comment = models.TextField()
	is_verified_purchase = models.BooleanField(default=False)
	is_approved = models.BooleanField(default=False, help_text="Approve review for public display")
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-created_at']
		verbose_name = "Product Review"
		verbose_name_plural = "Product Reviews"
	
	def __str__(self):
		return f"{self.customer_name} - {self.product.name} ({self.rating}★)"


# Wishlist model
class Wishlist(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ['user', 'product']
		ordering = ['-created_at']
		verbose_name = "Wishlist Item"
		verbose_name_plural = "Wishlist Items"
	
	def __str__(self):
		return f"{self.user.username} - {self.product.name}"


# Cart model
class Cart(models.Model):
	session_key = models.CharField(max_length=40, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart {self.session_key}"

# CartItem model
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"

# Extended Order model
class Order(models.Model):
	STATUS_CHOICES = [
		("pending", "Pending"),
		("paid", "Paid"),
		("failed", "Failed"),
	]
	# Cart reference
	cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
	# Customer info
	full_name = models.CharField(max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	country = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=20)
	delivery_method = models.CharField(max_length=30, choices=[("pickup", "Pickup"), ("delivery", "Delivery")], default="pickup")
	# Order summary
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order #{self.id} - {self.full_name}"

# Payment gateway abstraction
class PaymentGateway(models.Model):
	name = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	config = models.JSONField(blank=True, null=True)

	class Meta:
		abstract = True

# Mock IremboPay gateway (to be replaced with real API integration)
class MockIremboPayGateway(PaymentGateway):
	def process_payment(self, order: Order):
		# Simulate payment success for testing
		order.status = "paid"
		order.save()
		return True
