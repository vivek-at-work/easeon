# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-11-15 07:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tickets", "0006_reporting_dashboard")]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="unit_part_reports",
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        )
    ]
