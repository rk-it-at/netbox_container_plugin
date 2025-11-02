from django.db.models import Count
from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "NetworkView",
    "NetworkListView",
    "NetworkEditView",
    "NetworkDeleteView",
)


@register_model_view(models.Network)
class NetworkView(generic.ObjectView):
    queryset = models.Network.objects.all()
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    template_name = "netbox_containers/network.html"


@register_model_view(models.Network, "list", path="", detail=False)
class NetworkListView(generic.ObjectListView):
    queryset = (
        models.Network.objects
        .annotate(pod_count=Count("pods", distinct=True))
        .annotate(device_count=Count("devices", distinct=True))
        .annotate(vm_count=Count("virtual_machines", distinct=True))
        .order_by("name", "pk")
    )

    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    filterset_form = forms.NetworkFilterForm


@register_model_view(models.Network, "add", detail=False)
@register_model_view(models.Network, "edit")
class NetworkEditView(generic.ObjectEditView):
    queryset = models.Network.objects.all()
    form = forms.NetworkForm


@register_model_view(models.Network, "delete")
class NetworkDeleteView(generic.ObjectDeleteView):
    queryset = models.Network.objects.all()


@register_model_view(models.Network, "bulk_edit", path="bulk-edit", detail=False)
class NetworkBulkEditView(generic.BulkEditView):
    queryset = models.Network.objects.all()
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    form = forms.NetworkBulkEditForm


@register_model_view(models.Network, "bulk_delete", path="bulk-delete", detail=False)
class NetworkBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Network.objects.all()
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
