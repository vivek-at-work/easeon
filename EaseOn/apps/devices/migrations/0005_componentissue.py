# Generated by Django 2.2.13 on 2020-12-14 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0004_device_address_cosmetic_changes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(editable=False, max_length=40)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('version', models.CharField(default='v0', max_length=3)),
                ('componenet_code', models.CharField(max_length=100)),
                ('componenet_description', models.CharField(max_length=100)),
                ('issue_code', models.CharField(max_length=100)),
                ('issue_description', models.CharField(max_length=100)),
                ('priority', models.IntegerField(default=1)),
                ('order', models.IntegerField(default=1)),
                ('is_technician_verified', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_componentissue', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_issues', to='devices.Device')),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_componentissue', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Component Issue',
                'verbose_name_plural': 'Component Issue',
                'ordering': ['-id'],
            },
        ),
    ]
