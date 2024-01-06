# Generated by Django 4.2.6 on 2023-11-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0023_additionalinfo_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additionalinfo',
            old_name='description',
            new_name='description_1',
        ),
        migrations.AddField(
            model_name='additionalinfo',
            name='description_2',
            field=models.TextField(blank=True, default='', max_length=200, null=True),
        ),
    ]