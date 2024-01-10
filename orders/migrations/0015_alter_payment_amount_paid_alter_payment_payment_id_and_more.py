# Generated by Django 4.2.7 on 2023-12-16 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_delete_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(default='Pending', max_length=250),
        ),
    ]