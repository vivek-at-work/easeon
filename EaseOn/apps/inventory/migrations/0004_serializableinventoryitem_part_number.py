# Generated by Django 2.2.13 on 2020-11-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20200419_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='serializableinventoryitem',
            name='part_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
