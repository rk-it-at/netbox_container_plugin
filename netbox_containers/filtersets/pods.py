from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers import models


__all__ = (
    "PodFilterSet",
)


class PodFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = models.Pod
        fields = (
            "id",
            "name",
            "status",
            "user",
            "published_ports",
        )
