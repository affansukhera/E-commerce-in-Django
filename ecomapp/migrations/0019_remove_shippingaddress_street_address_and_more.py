# Generated by Django 4.2.6 on 2023-10-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0018_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='Street_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='Zip_code',
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='area_code',
            field=models.TextField(max_length=10),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='last_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='primary_phone',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='street_address',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.IntegerField(default=0),
        ),
    ]
