# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-12-26 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("slas", "0002_auto_20201226_2112"),
        ("tickets", "0021_auto_20201224_1528"),
    ]

    operations = [
        migrations.AddField(
            model_name="voucher",
            name="sla",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="vouchers",
                to="slas.SLA",
            ),
        )
    ]
