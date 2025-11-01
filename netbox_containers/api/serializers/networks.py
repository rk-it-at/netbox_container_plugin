from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "NetworkSerializer",
)


class NetworkSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Network
        fields = (
            "name",
            "driver",
            "user",
            "subnet",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "devices",
            "virtual_machines",
            "tags",
            "custom_fields",
        )
