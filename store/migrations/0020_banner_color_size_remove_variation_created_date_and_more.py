# Generated by Django 4.2.7 on 2023-12-27 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_variation_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/banner')),
                ('alt_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
                ('color_code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='variation',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='variation_category',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='variation_value',
        ),
        migrations.DeleteModel(
            name='ProductVariation',
        ),
        migrations.AddField(
            model_name='variation',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.color'),
        ),
        migrations.AddField(
            model_name='variation',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.size'),
        ),
    ]
