# Generated by Django 4.2.7 on 2023-12-28 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_banner_color_size_remove_variation_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='stock',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
