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
