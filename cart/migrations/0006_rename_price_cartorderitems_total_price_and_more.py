# Generated by Django 5.1.2 on 2024-12-02 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cartorderitems_invoice_num_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartorderitems',
            old_name='price',
            new_name='total_price',
        ),
        migrations.RenameField(
            model_name='cartorderitems',
            old_name='total',
            new_name='unit_price',
        ),
    ]