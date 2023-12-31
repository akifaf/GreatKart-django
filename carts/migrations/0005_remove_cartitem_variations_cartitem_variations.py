# Generated by Django 4.2.7 on 2023-12-20 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_variation_product_productvariation_product'),
        ('carts', '0004_cartitem_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.productvariation'),
        ),
    ]
