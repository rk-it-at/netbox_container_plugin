import django_tables2 as tables
from django.db.models import Count
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Network
from netbox_containers.models.networks import NetworkDriverChoices


__all__ = (
    "NetworkTable",
)


class NetworkTable(NetBoxTable):
    name = tables.Column(linkify=True,)
    driver = columns.ChoiceFieldColumn()
    user = tables.Column(linkify=True)
    subnet = tables.Column()
    pod_count = columns.LinkedCountColumn(
        accessor='pod_count',
        viewname='plugins:netbox_containers:pod_list',
        url_params={'networks_id': 'pk'}, 
        verbose_name="Pods",
        orderable=False,
    )
    device_count = columns.LinkedCountColumn(
        accessor="device_count",
        verbose_name="Devices",
        viewname="dcim:device_list",
        url_params={"container_networks_id": "pk"},
        orderable=False,
    )
    vm_count = columns.LinkedCountColumn(
        accessor="vm_count",
        verbose_name="Virtual machines",
        viewname="virtualization:virtualmachine_list",
        url_params={"container_networks_id": "pk"},
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = Network
        fields = (
            'pk',
            'name',
            'driver',
            'user',
            'subnet',
            "pod_count",
            "device_count",
            "vm_count"
        )
        default_columns = (
            'name', 'user', 'subnet', 'device_count', 'vm_count'
        )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
            .annotate(device_count=Count("devices", distinct=True))
            .annotate(vm_count=Count("virtual_machines", distinct=True))
        )
