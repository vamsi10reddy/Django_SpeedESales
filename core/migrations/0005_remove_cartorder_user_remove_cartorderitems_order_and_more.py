# Generated by Django 5.1.2 on 2024-11-21 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cartorderitems',
            name='order',
        ),
        migrations.RemoveField(
            model_name='cartorderitems',
            name='product',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='CartOrder',
        ),
        migrations.DeleteModel(
            name='CartOrderItems',
        ),
    ]
