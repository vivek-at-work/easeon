# -*- coding: utf-8 -*-
# Generated by Django 2.2.8 on 2020-03-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanerinventoryitem',
            name='serial_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='repairinventoryitem',
            name='serial_number',
            field=models.CharField(max_length=20),
        ),
    ]
