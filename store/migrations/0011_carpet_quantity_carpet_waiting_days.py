# Generated by Django 4.2.12 on 2024-05-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_cartitem_carpet_remove_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpet',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='carpet',
            name='waiting_days',
            field=models.IntegerField(default=0, verbose_name='Время ожидания в днях'),
        ),
    ]