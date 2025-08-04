from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class ProductCategory(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("is active"), default=True)
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("category"))
    description = models.TextField(_("description"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("image"), upload_to="products/")
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(_("transaction id"), max_length=100, unique=True)
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    status = models.CharField(_("status"), max_length=20, choices=ORDER_STATUS, default="pending")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Order #{self.id} - {self.amount}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

class ReusableCup(models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Reusable Cup")
        verbose_name_plural = _("Reusable Cups")

    def __str__(self):
        return self.name

