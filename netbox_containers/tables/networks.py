import django_tables2 as tables
from netbox.tables import NetBoxTable
from netbox_containers.models import Network


__all__ = (
    "NetworkTable",
)


class NetworkTable(NetBoxTable):
    name = tables.Column(
        linkify = True,
    )

    class Meta(NetBoxTable.Meta):
        model = Network
        fields = (
            'pk',
            'id',
            'name'
        )
        default_columns = (
            'name',
        )
