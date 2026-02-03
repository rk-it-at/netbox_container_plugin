import django_tables2 as tables
from django.db.models import Count
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Container
from netbox_containers.models.containers import ContainerStatusChoices


__all__ = (
    "ContainerTable",
)


class ContainerTable(NetBoxTable):
    name = tables.Column(linkify=True)
    image = tables.Column(
        accessor='image_tag.full_reference',
        verbose_name='Image',
    )
    status = columns.ChoiceFieldColumn()
    user = tables.Column(linkify=True)
    published_ports = tables.Column()
    pod = tables.Column(linkify=True)
    tags = columns.TagColumn()
    device_count = columns.LinkedCountColumn(
        accessor="device_count",
        verbose_name="Devices",
        viewname="dcim:device_list",
        url_params={"container_containers_id": "pk"},
        orderable=False,
    )
    vm_count = columns.LinkedCountColumn(
        accessor="vm_count",
        verbose_name="Virtual machines",
        viewname="virtualization:virtualmachine_list",
        url_params={"container_containers_id": "pk"},
        orderable=False,
    )
    command = tables.Column()
    user_namespace = tables.Column()
    memory_limit = tables.Column()
    cpu_limit = tables.Column()
    environment = tables.Column()
    add_host = tables.Column()
    is_infra = columns.BooleanColumn(verbose_name="Infra")

    class Meta(NetBoxTable.Meta):
        model = Container
        fields = (
            "pk",
            "name",
            "status",
            "user",
            "published_ports",
            "pod",
            "command",
            "user_namespaces",
            "memory_limit",
            "cpu_limit",
            "environment",
            "add_host",
            "is_infra",
            "device_count",
            "vm_count",
            "tags"
        )
        default_columns = ("name", "status", "pod", "is_infra", "published_ports", "device_count", "vm_count")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
            .annotate(device_count=Count("devices", distinct=True))
            .annotate(vm_count=Count("virtual_machines", distinct=True))
        )
