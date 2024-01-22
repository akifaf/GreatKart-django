# Generated by Django 4.2.7 on 2024-01-22 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_variationimage_alter_variation_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variationimage',
            name='product',
        ),
        migrations.AddField(
            model_name='variationimage',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.color'),
        ),
        migrations.AlterField(
            model_name='variationimage',
            name='image',
            field=models.ImageField(max_length=255, null=True, unique=True, upload_to='variation/products/'),
        ),
    ]
