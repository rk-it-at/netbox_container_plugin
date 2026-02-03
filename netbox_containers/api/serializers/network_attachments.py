from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "NetworkAttachmentSerializer",
)


class NetworkAttachmentSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.NetworkAttachment
        fields = (
            "container",
            "pod",
            "mode",
            "network",
            "options",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "custom_fields",
        )
