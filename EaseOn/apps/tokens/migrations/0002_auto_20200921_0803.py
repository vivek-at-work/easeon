# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-09-21 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='token',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='token',
            name='city',
        ),
        migrations.RemoveField(
            model_name='token',
            name='country',
        ),
        migrations.RemoveField(
            model_name='token',
            name='pin_code',
        ),
        migrations.RemoveField(
            model_name='token',
            name='state',
        ),
        migrations.RemoveField(
            model_name='token',
            name='street',
        ),
    ]
