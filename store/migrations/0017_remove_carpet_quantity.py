# Generated by Django 5.0.6 on 2024-05-26 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_carpet_size_carpetsize_delete_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carpet',
            name='quantity',
        ),
    ]
