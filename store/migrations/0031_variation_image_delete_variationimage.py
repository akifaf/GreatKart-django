# Generated by Django 4.2.7 on 2024-01-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_remove_cartitem_variation_image'),
        ('store', '0030_remove_variation_image_variationimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to='variation/products/'),
        ),
        migrations.DeleteModel(
            name='VariationImage',
        ),
    ]
