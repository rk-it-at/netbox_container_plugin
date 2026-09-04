from netbox.views import generic
from utilities.views import register_model_view

from netbox_containers import filtersets, forms, models, tables

__all__ = (
    "VolumeDeleteView",
    "VolumeEditView",
    "VolumeListView",
    "VolumeView",
)


@register_model_view(models.Volume)
class VolumeView(generic.ObjectView):
    queryset = models.Volume.objects.all()
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
    template_name = "netbox_containers/volume.html"
    form = forms.VolumeForm


@register_model_view(models.Volume, "list", path="", detail=False)
class VolumeListView(generic.ObjectListView):
    queryset = models.Volume.objects.all()
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
    filterset_form = forms.VolumeFilterForm


@register_model_view(models.Volume, "add", detail=False)
@register_model_view(models.Volume, "edit")
class VolumeEditView(generic.ObjectEditView):
    queryset = models.Volume.objects.all()
    form = forms.VolumeForm


@register_model_view(models.Volume, "delete")
class VolumeDeleteView(generic.ObjectDeleteView):
    queryset = models.Volume.objects.all()


@register_model_view(models.Volume, "bulk_edit", path="bulk-edit", detail=False)
class VolumeBulkEditView(generic.BulkEditView):
    queryset = models.Volume.objects.all()
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
    form = forms.VolumeBulkEditForm


@register_model_view(models.Volume, "bulk_delete", path="bulk-delete", detail=False)
class VolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Volume.objects.all()
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
