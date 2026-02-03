import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Secret


__all__ = (
    "SecretTable",
)


class SecretTable(NetBoxTable):
    name = tables.Column(linkify=True)
    driver = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Secret
        fields = (
            "pk",
            "name",
            "driver",
            "tags",
        )
        default_columns = ("name", "driver")
