from .import_resources import (
    LoanerInventoryItemAdmin,
    RepairInventoryItemAdmin,
    SerializableInventoryItemAdmin,
)
from inventory.models import (
    LoanerInventoryItem,
    RepairInventoryItem,
    SerializableInventoryItem,
)
from core.admin import register

register(LoanerInventoryItem, LoanerInventoryItemAdmin)
register(RepairInventoryItem, RepairInventoryItemAdmin)
register(SerializableInventoryItem, SerializableInventoryItemAdmin)
