import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Mount


__all__ = (
    "MountTable",
)


class MountTable(NetBoxTable):
    container = tables.Column(linkify=True)
    mount_type = tables.Column(verbose_name="Type")
    source = tables.Column(accessor="source", verbose_name="Source")
    dest_path = tables.Column(verbose_name="Destination")
    options = tables.Column(verbose_name="Options")

    class Meta(NetBoxTable.Meta):
        model = Mount
        fields = (
            "pk",
            "container",
            "mount_type",
            "source",
            "dest_path",
            "options",
            "tags"
        )
        default_columns = ("container", "mount_type", "source", "dest_path", "options")
