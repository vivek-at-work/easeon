# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-12-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("devices", "0003_auto_20201213_1513")]

    operations = [
        migrations.AddField(
            model_name="device",
            name="address_cosmetic_changes",
            field=models.BooleanField(default=False),
        )
    ]
