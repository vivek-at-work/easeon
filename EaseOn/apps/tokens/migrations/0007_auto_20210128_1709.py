# Generated by Django 2.2.13 on 2021-01-28 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0006_token_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='distance_from_organization',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='latitude',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='longitude',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
