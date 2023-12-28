# Generated by Django 4.2.7 on 2023-12-28 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_banner_color_size_remove_variation_created_date_and_more'),
        ('orders', '0019_orderproduct_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
