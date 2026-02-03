import django_filters as filters
from django_filters import CharFilter, ModelMultipleChoiceFilter
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Container, Pod


__all__ = (
    "ContainerFilterSet",
)


class ContainerFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')

    status = filters.MultipleChoiceFilter(
        choices=Container._meta.get_field("status").choices
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
    pod = filters.ModelChoiceFilter(
        queryset=Pod.objects.all()
    )
    pod_id = filters.NumberFilter(field_name="pod_id")
    network_id = filters.NumberFilter(method="filter_network")
    is_infra = filters.BooleanFilter()

    class Meta:
        model = Container
        fields = (
            "id",
            "name",
            "status",
            "user",
            "published_ports",
            "pod",
            "pod_id",
            "is_infra",
            "network_id",
            "devices",
            "virtual_machines",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)

    def filter_network(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(network_attachments__network_id=value)
