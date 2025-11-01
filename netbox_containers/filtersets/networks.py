from django_filters import CharFilter, ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from ipam.models import Prefix
from netbox_containers import models


__all__ = (
    "NetworkFilterSet",
)


class NetworkFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')

    devices = ModelMultipleChoiceFilter(
        field_name="devices",
        queryset=Device.objects.all(),
        label="Devices",
    )
    virtual_machines = ModelMultipleChoiceFilter(
        field_name="virtual_machines",
        queryset=VirtualMachine.objects.all(),
        label="Virtual machines",
    )
    prefixes = ModelMultipleChoiceFilter(
        field_name='prefixes',
        queryset=Prefix.objects.all(),
        label='Prefixes',
    )

    class Meta:
        model = models.Network
        fields = (
            "id",
            "name",
            "driver",
            "user",
            "devices",
            "virtual_machines",
            "prefixes",
            "label",
            "gateway",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
