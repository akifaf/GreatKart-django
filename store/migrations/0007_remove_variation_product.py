# Generated by Django 4.2.7 on 2023-12-17 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_variation_stock_productvariation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
    ]
