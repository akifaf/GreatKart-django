# Generated by Django 4.2.7 on 2023-12-05 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='varitation_category',
            new_name='variation_category',
        ),
    ]
