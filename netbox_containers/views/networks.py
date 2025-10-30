from django.db.models import Count
from netbox.views import generic
from utilities.views import register_model_view
#from netbox_containers import filtersets, forms, models, tables
from netbox_containers import filtersets, models, tables


__all__ = (
    "NetworkView",
    "NetworkListView",
)


@register_model_view(models.Network, "list", path="", detail=False)
class NetworkListView(generic.ObjectListView):
    queryset = models.Network.objects.all()
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet


@register_model_view(models.Network)
class NetworkView(generic.ObjectView):
    queryset = models.Network.objects.all()
#    table = tables.NetworkTable
