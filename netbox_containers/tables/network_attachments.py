import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import NetworkAttachment


__all__ = (
    "NetworkAttachmentTable",
)


class NetworkAttachmentTable(NetBoxTable):
    mode = columns.ChoiceFieldColumn()
    network = tables.Column(linkify=True)
    options = tables.Column()
    container = tables.Column(linkify=True)
    pod = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = NetworkAttachment
        fields = (
            "pk",
            "container",
            "pod",
            "mode",
            "network",
            "options",
            "tags",
        )
        default_columns = ("container", "pod", "mode", "network", "options")
