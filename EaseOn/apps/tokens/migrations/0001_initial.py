# -*- coding: utf-8 -*-
# Generated by Django 2.2.8 on 2020-02-25 18:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.ORGANIZATIONS_ORGANIZATION_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("guid", models.CharField(editable=False, max_length=40)),
                ("version", models.CharField(default="v0", max_length=3)),
                ("location_code", models.CharField(max_length=100)),
                ("token_number", models.CharField(max_length=100)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("country", models.CharField(blank=True, max_length=50, null=True)),
                ("state", models.CharField(blank=True, max_length=50, null=True)),
                ("address_line_1", models.CharField(max_length=60)),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                ("street", models.CharField(blank=True, max_length=60, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "contact_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("pin_code", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_token",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="modified_token",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="tokens",
                        to=settings.ORGANIZATIONS_ORGANIZATION_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-updated_at", "-created_at"),
                "get_latest_by": "created_at",
                "abstract": False,
            },
        )
    ]
