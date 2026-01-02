from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "VolumeSerializer",
)


class VolumeSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Volume
        fields = (
            "name",
            "driver",
            "label",
            "options",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "comments",
            "custom_fields",
        )
