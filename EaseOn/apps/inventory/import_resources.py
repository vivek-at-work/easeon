# -*- coding: utf-8 -*-
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from inventory.models import (
    LoanerInventoryItem,
    RepairInventoryItem,
    SerializableInventoryItem,
)


class LoanerInventoryItemResource(resources.ModelResource):
    class Meta:
        model = LoanerInventoryItem


class LoanerInventoryItemAdmin(ImportExportModelAdmin):
    resource_class = LoanerInventoryItemResource


class RepairInventoryItemResource(resources.ModelResource):
    class Meta:
        model = RepairInventoryItem


class RepairInventoryItemAdmin(ImportExportModelAdmin):
    resource_class = RepairInventoryItemResource


class SerializableInventoryItemResource(resources.ModelResource):
    class Meta:
        model = SerializableInventoryItem


class SerializableInventoryItemAdmin(ImportExportModelAdmin):
    resource_class = SerializableInventoryItemResource
