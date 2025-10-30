import django_tables2 as tables
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

    class Meta(NetBoxTable.Meta):
        model = Pod
        fields = (
            "pk",
            "name",
            "status",
            "user",
            "published_ports",
        )
        default_columns = ("name", "status", "published_ports")
