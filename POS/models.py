from django.db import models
from Inventory.models import  *
from django.contrib.auth.models import User  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    invoice_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()

    def __str__(self):
        return f"Order {self.invoice_number} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


# Create your models here.
