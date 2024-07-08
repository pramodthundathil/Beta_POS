from django.db import models
from Inventory.models import  *
from django.contrib.auth.models import User  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    invoice_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)  # Set default to 0
    total_tax = models.FloatField(default=0)
    payment_status = models.BooleanField(default=False)

    def update_totals(self):
        # Calculate total amount and total tax from associated OrderItems
        total_amount = 0
        total_tax = 0
        for item in self.orderitem_set.all():
            total_amount += item.total_price
            total_tax += item.total_tax
        
        self.total_amount = total_amount
        self.total_tax = total_tax
        self.save()

    def __str__(self):
        return f"Order {self.invoice_number} by {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField()
    total_price = models.FloatField(editable=False)  # Make this field non-editable
    total_tax = models.FloatField(editable=False)  # Make this field non-editable

    # Example tax rate of 10%

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price  # Assuming the product has a price field
        self.total_price = self.unit_price * self.quantity
        self.total_tax = self.tax_amount * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


# Create your models here.
