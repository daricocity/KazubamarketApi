# Generated by Django 2.1 on 2020-11-04 23:19

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload image file size of 300x300', null=True, upload_to=products.models.upload_product_image_path),
        ),
    ]
