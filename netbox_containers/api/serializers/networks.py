from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ipam.models import Prefix
from netbox_containers import models


__all__ = (
    "NetworkSerializer",
)


class NetworkSerializer(NetBoxModelSerializer):
    prefixes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Prefix.objects.all(), required=False
    )
    effective_subnets = serializers.SerializerMethodField(read_only=True)

    def get_effective_subnets(self, obj):
        return obj.effective_subnets

    class Meta:
        model = models.Network
        fields = (
            "name",
            "driver",
            "user",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "devices",
            "virtual_machines",
            "prefixes",
            "effective_subnets",
            "tags",
            "custom_fields",
        )
