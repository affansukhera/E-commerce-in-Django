# Generated by Django 4.2.5 on 2023-10-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_rename_is_active_product_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
