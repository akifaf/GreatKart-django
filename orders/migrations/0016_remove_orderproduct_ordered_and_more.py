# Generated by Django 4.2.7 on 2023-12-16 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_variation_stock_productvariation'),
        ('orders', '0015_alter_payment_amount_paid_alter_payment_payment_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
