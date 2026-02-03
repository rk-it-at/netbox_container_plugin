import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import ContainerSecret


__all__ = (
    "ContainerSecretTable",
)


class ContainerSecretTable(NetBoxTable):
    container = tables.Column(linkify=True)
    secret = tables.Column(linkify=True)
    type = columns.ChoiceFieldColumn()
    target = tables.Column()
    uid = tables.Column()
    gid = tables.Column()
    mode = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = ContainerSecret
        fields = (
            "pk",
            "container",
            "secret",
            "type",
            "target",
            "uid",
            "gid",
            "mode",
            "tags",
        )
        default_columns = ("container", "secret", "type", "target", "uid", "gid", "mode")
