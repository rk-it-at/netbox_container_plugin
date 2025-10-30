from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers import models


__all__ = (
    "NetworkFilterSet",
)


class NetworkFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = models.Network
        fields = (
            "id",
            "name",
        )
