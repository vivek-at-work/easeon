# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-09-22 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tokens', '0002_auto_20200921_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='counter_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='invited_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='received_tokens',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
