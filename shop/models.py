
from django.db import models

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
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="RWF")
	is_active = models.BooleanField(default=True)
	image = models.ImageField(upload_to="product_images/", blank=True, null=True)

	def __str__(self):
		return self.name


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
