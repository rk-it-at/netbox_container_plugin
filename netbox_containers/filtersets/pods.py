##from django.db.models import Q
from django_filters import CharFilter
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers import models


__all__ = (
    "PodFilterSet",
)


class PodFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')
    class Meta:
        model = models.Pod
        fields = (
            "id",
            "name",
            "status",
            "user",
            "published_ports",
            "networks"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
