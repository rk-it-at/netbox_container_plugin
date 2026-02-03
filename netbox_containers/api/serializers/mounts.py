from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "MountSerializer",
)


class MountSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Mount
        fields = (
            "container",
            "mount_type",
            "volume",
            "host_path",
            "dest_path",
            "options",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "custom_fields",
        )
