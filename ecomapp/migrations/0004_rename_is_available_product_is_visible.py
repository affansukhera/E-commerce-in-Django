# Generated by Django 4.2.5 on 2023-10-06 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_product_discount_percentage_alter_product_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_available',
            new_name='is_visible',
        ),
    ]
