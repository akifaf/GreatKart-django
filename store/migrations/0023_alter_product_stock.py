# Generated by Django 4.2.7 on 2024-01-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_coupon_alter_color_color_alter_color_color_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
