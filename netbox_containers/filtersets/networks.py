from django_filters import CharFilter, ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
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

    class Meta:
        model = models.Network
        fields = (
            "id",
            "name",
            "driver",
            "user",
            "subnet",
            "devices",
            "virtual_machines"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
