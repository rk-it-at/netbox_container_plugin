from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_containers import models


__all__ = (
    "ImageSerializer",
    "ImageTagSerializer",
)


class ImageSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            "name",
            "registry",
            "default_tag",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "comments",
            "custom_fields",
        )


class ImageTagSerializer(NetBoxModelSerializer):

    class Meta:
        model = models.ImageTag
        fields = (
            "image",
            "image_tag",
            "os",
            "arch",
            "id",
            "url",
            "display",
            "created",
            "last_updated",
            "tags",
            "comments",
            "custom_fields",
        )
