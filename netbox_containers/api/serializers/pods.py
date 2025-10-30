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
        )
