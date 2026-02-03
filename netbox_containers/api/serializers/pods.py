from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "PodSerializer",
)


class PodSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Pod
        fields = (
            "name",
            "status",
            "user",
            "published_ports",
            "infra_container",
            "devices",
            "virtual_machines",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "comments",
            "custom_fields",
        )
