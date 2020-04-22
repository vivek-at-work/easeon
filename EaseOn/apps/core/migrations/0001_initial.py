# Generated by Django 2.2.8 on 2020-02-25 18:01

import core.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=100, unique=True, validators=[core.models.user.validate_user_email_domain])),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'SuperUser'), (2, 'Operator'), (3, 'TokenUser')], default=2)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('pin_code', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=16)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('is_email_verified_by_user', models.BooleanField(default=False)),
                ('email_confirmation_mail_sent_on', models.DateTimeField(null=True)),
                ('account_activation_mail_sent_to_admin', models.DateTimeField(null=True)),
                ('account_activation_replied_by_admin', models.DateTimeField(null=True)),
                ('deactivated_on', models.DateTimeField(null=True)),
                ('next_password_change_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('gsx_technician_id', models.CharField(max_length=100)),
                ('gsx_user_name', models.CharField(max_length=100)),
                ('gsx_auth_token', models.CharField(max_length=100)),
                ('gsx_token_last_refreshed_on', models.DateTimeField(null=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
