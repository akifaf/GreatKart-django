# Generated by Django 4.2.7 on 2023-12-16 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_variation_stock_productvariation'),
        ('orders', '0016_remove_orderproduct_ordered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
