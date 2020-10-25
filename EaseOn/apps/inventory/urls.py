# -*- coding: utf-8 -*-
from inventory.viewsets import (
    LoanerItemViewSet,
    PenaltyAmountViewSet,
    RepairItemViewSet,
    SerializableItemViewSet,
)
from rest_framework import routers

inventory_router = routers.DefaultRouter()
base = "inventory"
inventory_router.register(
    r"{0}/loaners".format(base), LoanerItemViewSet, basename="loanerinventoryitem"
)
inventory_router.register(
    r"{0}/repairs".format(base), RepairItemViewSet, basename="repairinventoryitem"
)
inventory_router.register(
    r"{0}/serializables".format(base),
    SerializableItemViewSet,
    basename="serializableinventoryitem",
)
inventory_router.register(
    r"{0}/penalty".format(base),
    PenaltyAmountViewSet,
    basename="loaneritempenaltyamount",
)
