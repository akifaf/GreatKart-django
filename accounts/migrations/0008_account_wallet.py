# Generated by Django 4.2.7 on 2023-12-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
