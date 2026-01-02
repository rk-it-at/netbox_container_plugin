import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from netbox_containers.models import Volume


__all__ = (
    "VolumeTable",
)


class VolumeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    driver = columns.ChoiceFieldColumn()
    label = tables.Column()
    options = tables.Column()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Volume
        fields = (
            "pk",
            "name",
            "driver",
            "label",
            "options",
            "tags"
        )
        default_columns = ("name", "driver", "label")
