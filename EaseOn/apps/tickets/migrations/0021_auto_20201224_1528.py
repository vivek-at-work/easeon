# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-12-24 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("tickets", "0020_orderline_componenet_issue")]

    operations = [
        migrations.RenameField(
            model_name="orderline",
            old_name="componenet_issue",
            new_name="component_issue",
        )
    ]
