# Generated by Django 2.2.13 on 2021-01-31 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0026_ticket_estimation'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_done_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='deliveries_done', to=settings.AUTH_USER_MODEL),
        ),
    ]
