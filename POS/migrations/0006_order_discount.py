# Generated by Django 5.0.7 on 2024-10-05 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0005_order_balance_amount_order_payed_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
