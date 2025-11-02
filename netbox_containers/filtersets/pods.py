import django_filters as filters
from django_filters import CharFilter, ModelMultipleChoiceFilter
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Pod


__all__ = (
    "PodFilterSet",
)


class PodFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')

    status = filters.MultipleChoiceFilter(
        choices=Pod._meta.get_field("status").choices
    )
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
        model = Pod
        fields = (
            "id",
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "devices",
            "virtual_machines",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
