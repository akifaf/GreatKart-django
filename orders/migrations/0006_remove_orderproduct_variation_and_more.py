# Generated by Django 4.2.7 on 2023-12-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_varitation_category_variation_variation_category'),
        ('orders', '0005_remove_orderproduct_color_remove_orderproduct_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]