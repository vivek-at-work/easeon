# Generated by Django 2.2.13 on 2020-11-19 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_serializableinventoryitem_part_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loanerinventoryitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Loaner Inventory Item', 'verbose_name_plural': 'Loaner Inventory Items'},
        ),
        migrations.AlterModelOptions(
            name='repairinventoryitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Repair Inventory Item', 'verbose_name_plural': 'Repair Inventory Items'},
        ),
        migrations.AlterModelOptions(
            name='serializableinventoryitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Non Serialized Inventory Item', 'verbose_name_plural': 'Non Serialized Inventory Items'},
        ),
    ]
