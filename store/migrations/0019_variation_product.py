# Generated by Django 4.2.7 on 2023-12-22 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_productvariation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
