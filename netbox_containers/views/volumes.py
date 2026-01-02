from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets
from netbox_containers.models.volumes import VolumeDriverChoices


__all__ = (
    "VolumeView",
    "VolumeListView",
    "VolumeEditView",
    "VolumeDeleteView",
)


@register_model_view(models.Volume)
class VolumeView(generic.ObjectView):
    queryset = models.Volume.objects.all()
    table = tables.VolumeTable
    filterset = filtersets.VolumeFilterSet
    template_name = "netbox_containers/volume.html"
    form = forms.VolumeForm

    def get_extra_context(self, request, instance):
        return {
            "VolumeDriverChoices": VolumeDriverChoices,  # expose colors mapping to the template
        }


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


@register_model_view(models.Volume, "changelog", path="changelog")
class VolumeChangeLogView(generic.ObjectChangeLogView):
    queryset = models.Volume.objects.all()


@register_model_view(models.Volume, "journal", path="journal")
class VolumeJournalView(generic.ObjectJournalView):
    queryset = models.Volume.objects.all()
