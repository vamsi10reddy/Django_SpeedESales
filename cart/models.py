from django.db import models
from django.conf import settings
import uuid
from core.models import Product  # You still need a relationship with Product

STATUS_CHOICE = (
    ("process", 'Processing'),
    ("shipped", 'Shipped'),
    ("delivered", 'Delivered'),
)

class CartOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="process")

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        verbose_name_plural = 'Cart Orders'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.order} contains {self.qty} of {self.product}"

    class Meta:
        verbose_name_plural = 'Cart Order Items'
        unique_together = ['order', 'product']        


class Address(models.Model):
    order = models.OneToOneField(CartOrder,  on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    send_to = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True)
    zipCode = models.CharField(max_length=25)
    status = models.BooleanField(default=False)
