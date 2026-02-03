from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "SecretSerializer",
)


class SecretSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.Secret
        fields = (
            "name",
            "driver",
            "options",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "custom_fields",
        )
