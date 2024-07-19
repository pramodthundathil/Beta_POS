from django.db import models
from django.contrib.auth.models import User 



class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=20)
    # image = models.FileField(upload_to='category_images')
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(
        max_length=15,
        # validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    gst_number = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(15), MaxLengthValidator(15)])
    city = models.CharField(max_length=255)
    state = models.CharField(null=True,max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    contact_info = models.TextField(blank=True, null=True)
    supply_product = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staus = models.BooleanField(default=True)



from django.db import models

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='foodimage')
    price = models.FloatField()
    status = models.BooleanField(default=True)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)

    # Additional fields
    price_before_tax = models.FloatField(null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)

    # Tax calculation
    TAX_CHOICES = (
        ("Inclusive", "Inclusive"),
        ("Exclusive", "Exclusive"),
    )
    tax = models.CharField(max_length=20, choices=TAX_CHOICES)
    tax_value = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None:
            self.price = float(self.price)  # Ensure self.price is a float
            if self.tax_value:
                tax_rate = self.tax_value.tax_percentage / 100
                if self.tax == "Exclusive":
                    self.tax_amount = round(self.price * tax_rate, 2)
                    self.price_before_tax = round(self.price, 2)
                    self.price = round(self.price + self.tax_amount, 2)
                elif self.tax == "Inclusive":
                    self.price_before_tax = round(self.price / (1 + tax_rate), 2)
                    self.tax_amount = round(self.price - self.price_before_tax, 2)
            else:
                self.price_before_tax = round(self.price, 2)
                self.tax_amount = 0.0
        else:
            self.price_before_tax = 0.0
            self.tax_amount = 0.0

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    gst_number = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(15), MaxLengthValidator(15)])
    city = models.CharField(max_length=255)
    state = models.CharField(null=True,max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    contact_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    staus = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
    

class PurchaseOrder(models.Model):
    PURCHASE_TYPES = [
        ('VAT', 'VAT'),
        ('GST', 'GST'),
        ('NO-TAX', 'NO-TAX'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]
    
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPES)
    bill_date = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateTimeField()
    supplier = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    place_of_supply = models.CharField(max_length=100)
    purchase_item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    discount = models.FloatField(help_text='in %', null=True, blank=True)
    tax = models.FloatField()
    cess = models.FloatField()
    amount = models.FloatField()
    status = models.BooleanField(default=True)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"PurchaseOrder {self.id} - {self.supplier}"
    



class Purchase(models.Model):
    PURCHASE_TYPES = [
        ('VAT', 'VAT'),
        ('GST', 'GST'),
        ('NO-TAX', 'NO-TAX'),
    ]
    PAYMENT_STATUS = (
        ("UNPAID","UNPAID"),
        ("PAID","PAID"),
        ("PARTIALLY","PARTIALLY")
    )
    
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPES)
    bill_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    payment_terms = models.IntegerField(help_text='Number of days, Credit Period', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    place_of_supply = models.CharField(max_length=100)
    purchase_bill_number = models.CharField(max_length=255, null=True, blank=True)
    purchase_order_number = models.CharField(max_length=20, null=True, blank=True)
    purchase_order_date = models.DateField(null=True, blank=True)
    purchase_item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    discount = models.FloatField(help_text='in %', null=True, blank=True)
    tax = models.FloatField()
    amount = models.FloatField()
    paid_amount = models.FloatField()
    balance_amount = models.FloatField()
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS)
    shipping_cost = models.FloatField(null=True, blank=True)
    recived_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier}"






