# Generated by Django 4.2.7 on 2023-12-22 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_color_size_rename_is_active_variation_is_available_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.RenameField(
            model_name='variation',
            old_name='is_available',
            new_name='is_active',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='color',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='size',
        ),
        migrations.AddField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], default='color', max_length=100),
        ),
        migrations.AddField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.AddField(
            model_name='productvariation',
            name='product_variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
