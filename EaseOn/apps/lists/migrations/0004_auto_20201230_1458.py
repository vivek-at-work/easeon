# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-12-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lists", "0003_auto_20200728_1848")]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="list_name",
            field=models.CharField(
                choices=[
                    ("TICKET_STATUS", "Ticket Status"),
                    ("COVERAGE_TYPE", "Coverage Type"),
                    ("GSX_SERVICE_TYPE", "GSX Service Type"),
                    ("REPAIR_TYPE", "Repair Type"),
                    ("GSX_REPAIR_TYPE", "GSX Repair Type"),
                    ("CUSTOMER_TYPE", "Customer Type"),
                    ("UNIT_PART", "Unit Part"),
                    ("STATES", "States"),
                    ("COUNTRY", "COUNTRY"),
                    ("SERIALIZABLE_INVENTORY_ITEM", "Serializable Inventory Item"),
                    ("LOANER_INVENTORY_PART_NUMBERS", "Loaner Inventory Part Numbers"),
                    (
                        "LOANER_INVENTORY_PENALTY_REASONS",
                        "Loaner Inventory Penalty Reasons",
                    ),
                    ("CONSIGNMENT_TYPE", "Consignment Types"),
                    ("REPORT_TYPES", "Report Types"),
                    ("FEEDBACK_PARAM", "Feedback Parameter"),
                ],
                default="TICKET_STATUS",
                max_length=100,
            ),
        )
    ]
