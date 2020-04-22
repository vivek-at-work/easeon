# Generated by Django 2.2.8 on 2020-02-25 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.ORGANIZATIONS_ORGANIZATION_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SerializableInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(editable=False, max_length=40)),
                ('version', models.CharField(default='v0', max_length=3)),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('available_quantity', models.IntegerField(default=0)),
                ('consumed_quantity', models.IntegerField(default=0)),
                ('consignment_type', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_serializableinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_serializableinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serializable_inventory_items', to=settings.ORGANIZATIONS_ORGANIZATION_MODEL)),
            ],
            options={
                'ordering': ('-updated_at', '-created_at'),
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RepairInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(editable=False, max_length=40)),
                ('version', models.CharField(default='v0', max_length=3)),
                ('serial_number', models.CharField(max_length=20, unique=True)),
                ('po_number', models.CharField(max_length=50)),
                ('awb_number', models.CharField(max_length=50)),
                ('part_number', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('consumed', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('consignment_type', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_repairinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_repairinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_inventory_items', to=settings.ORGANIZATIONS_ORGANIZATION_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanerItemPenaltyAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(editable=False, max_length=40)),
                ('version', models.CharField(default='v0', max_length=3)),
                ('part_number', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=100)),
                ('cost', models.FloatField(default=0.0)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_loaneritempenaltyamount', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_loaneritempenaltyamount', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated_at', '-created_at'),
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanerInventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guid', models.CharField(editable=False, max_length=40)),
                ('version', models.CharField(default='v0', max_length=3)),
                ('serial_number', models.CharField(max_length=20, unique=True)),
                ('po_number', models.CharField(max_length=50)),
                ('awb_number', models.CharField(max_length=50)),
                ('part_number', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('consumed', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_loanerinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_loanerinventoryitem', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loaner_inventory_items', to=settings.ORGANIZATIONS_ORGANIZATION_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
