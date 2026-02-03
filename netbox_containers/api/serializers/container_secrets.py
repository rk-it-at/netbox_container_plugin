from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "ContainerSecretSerializer",
)


class ContainerSecretSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.ContainerSecret
        fields = (
            "container",
            "secret",
            "type",
            "target",
            "uid",
            "gid",
            "mode",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "custom_fields",
        )
