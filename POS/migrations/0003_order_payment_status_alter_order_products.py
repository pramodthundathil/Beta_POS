# Generated by Django 5.0.4 on 2024-07-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0006_customer'),
        ('POS', '0002_alter_order_customer_alter_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='POS.OrderItem', to='Inventory.product'),
        ),
    ]