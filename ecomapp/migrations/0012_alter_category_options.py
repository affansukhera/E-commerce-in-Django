# Generated by Django 4.2.6 on 2023-10-17 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0011_alter_product_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
    ]