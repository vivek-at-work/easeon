# -*- coding: utf-8 -*-
from core.admin import register
from inventory.models import (
    LoanerInventoryItem,
    RepairInventoryItem,
    SerializableInventoryItem,
)

from .import_resources import (
    LoanerInventoryItemAdmin,
    RepairInventoryItemAdmin,
    SerializableInventoryItemAdmin,
)

register(LoanerInventoryItem, LoanerInventoryItemAdmin)
register(RepairInventoryItem, RepairInventoryItemAdmin)
register(SerializableInventoryItem, SerializableInventoryItemAdmin)
