# Generated by Django 4.2.7 on 2024-01-04 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cart_created_at_remove_cartitem_ordered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Item Added'), (1, 'Item Removed'), (2, 'Item Checkout')], default=0, null=True),
        ),
    ]
