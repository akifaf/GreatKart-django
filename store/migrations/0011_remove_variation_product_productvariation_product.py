# Generated by Django 4.2.7 on 2023-12-19 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_productvariation_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.AddField(
            model_name='productvariation',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
