from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "ContainerSerializer",
)


class ContainerSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Container
        fields = (
            "name",
            "image_tag",
            "status",
            "user",
            "published_ports",
            "pod",
            "is_infra",
            "command",
            "user_namespaces",
            "memory_limit",
            "cpu_limit",
            "environment",
            "add_host",
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
