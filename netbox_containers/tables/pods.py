import django_tables2 as tables
from django.db.models import Count
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Pod
from netbox_containers.models.pods import PodStatusChoices


__all__ = (
    "PodTable",
)


class PodTable(NetBoxTable):
    name = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn()
    user = tables.Column(linkify=True)
    published_ports = tables.Column()
    tags = columns.TagColumn()
    container_count = columns.LinkedCountColumn(
        accessor="container_count",
        verbose_name="Containers",
        viewname="plugins:netbox_containers:container_list",
        url_params={"pod_id": "pk"},
        orderable=False,
    )
    device_count = columns.LinkedCountColumn(
        accessor="device_count",
        verbose_name="Devices",
        viewname="dcim:device_list",
        url_params={"container_pods_id": "pk"},
        orderable=False,
    )
    vm_count = columns.LinkedCountColumn(
        accessor="vm_count",
        verbose_name="Virtual machines",
        viewname="virtualization:virtualmachine_list",
        url_params={"container_pods_id": "pk"},
        orderable=False,
    )

    class Meta(NetBoxTable.Meta):
        model = Pod
        fields = (
            "pk",
            "name",
            "status",
            "user",
            "published_ports",
            "container_count",
            "device_count",
            "vm_count",
            "tags"
        )
        default_columns = ("name", "status", "published_ports", "container_count", "device_count", "vm_count")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(container_count=Count("containers", distinct=True))
