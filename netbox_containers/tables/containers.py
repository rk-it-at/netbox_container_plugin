import django_tables2 as tables
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
    networks = tables.ManyToManyColumn(linkify_item=True)
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

    class Meta(NetBoxTable.Meta):
        model = Container
        fields = (
            "pk",
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "pod",
            "device_count",
            "vm_count",
            "tags"
        )
        default_columns = ("name", "status", "pod", "published_ports", "device_count", "vm_count")
