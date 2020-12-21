# Generated by Django 2.2.13 on 2020-11-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_auto_20201129_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='customer_signature',
            field=models.ImageField(blank=True, null=True, upload_to='customer_signatures/vouchers'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='customer_signature',
            field=models.ImageField(blank=True, null=True, upload_to='customer_signatures/deliveries'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='customer_signature',
            field=models.ImageField(blank=True, null=True, upload_to='customer_signatures/tickets'),
        ),
    ]
