# -*- coding: utf-8 -*-
# Generated by Django 2.2.13 on 2020-08-28 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200729_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
