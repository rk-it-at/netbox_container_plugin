from django.db.models import Count
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from netbox_containers import filtersets, models

from . import serializers


class ContainersRootView(APIRootView):
    def get_view_name(self):
        return "Containers Plugin"


class PodViewSet(NetBoxModelViewSet):
    queryset = models.Pod.objects.all()

    serializer_class = serializers.PodSerializer
    filterset_class = filtersets.PodFilterSet


class NetworkViewSet(NetBoxModelViewSet):
    queryset = models.Network.objects.all()

    serializer_class = serializers.NetworkSerializer
    filterset_class = filtersets.NetworkFilterSet


class ImageViewSet(NetBoxModelViewSet):
    queryset = models.Image.objects.all()

    serializer_class = serializers.ImageSerializer
    filterset_class = filtersets.ImageFilterSet


class ImageTagViewSet(NetBoxModelViewSet):
    queryset = models.ImageTag.objects.all()

    serializer_class = serializers.ImageTagSerializer
    filterset_class = filtersets.ImageTagFilterSet


class VolumeViewSet(NetBoxModelViewSet):
    queryset = models.Volume.objects.all()

    serializer_class = serializers.VolumeSerializer
    filterset_class = filtersets.VolumeFilterSet
