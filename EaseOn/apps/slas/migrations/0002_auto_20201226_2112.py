# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-12-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("slas", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="sla",
            name="sla_type",
            field=models.CharField(
                choices=[
                    ("TICKET_SLA", "Ticket SLA"),
                    ("DELIVERY_SLA", "Delivery SLA"),
                    ("PHONE_LOAN_AGREEMENT", "Phone Loan Agreement"),
                    ("VOUCHER_SLA", "Voucher Agreement"),
                ],
                default="TICKET_SLA",
                max_length=100,
            ),
        )
    ]
