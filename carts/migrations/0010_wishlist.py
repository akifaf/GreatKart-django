# Generated by Django 4.2.7 on 2024-01-02 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_coupon_alter_color_color_alter_color_color_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0009_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
