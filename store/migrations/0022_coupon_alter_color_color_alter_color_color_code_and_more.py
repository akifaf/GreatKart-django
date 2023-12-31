# Generated by Django 4.2.7 on 2023-12-29 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_variation_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=20)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=500)),
            ],
        ),
        migrations.AlterField(
            model_name='color',
            name='color',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='color_code',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
