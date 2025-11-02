from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets
from netbox_containers.models.pods import PodStatusChoices


__all__ = (
    "PodView",
    "PodListView",
    "PodEditView",
    "PodDeleteView",
)


@register_model_view(models.Pod)
class PodView(generic.ObjectView):
    queryset = models.Pod.objects.all()
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
    template_name = "netbox_containers/pod.html"
    form = forms.PodForm

    def get_extra_context(self, request, instance):
        return {
            "PodStatusChoices": PodStatusChoices,  # expose colors mapping to the template
        }


@register_model_view(models.Pod, "list", path="", detail=False)
class PodListView(generic.ObjectListView):
    queryset = models.Pod.objects.all()
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
    filterset_form = forms.PodFilterForm


@register_model_view(models.Pod, "add", detail=False)
@register_model_view(models.Pod, "edit")
class PodEditView(generic.ObjectEditView):
    queryset = models.Pod.objects.all()
    form = forms.PodForm


@register_model_view(models.Pod, "delete")
class PodDeleteView(generic.ObjectDeleteView):
    queryset = models.Pod.objects.all()


@register_model_view(models.Pod, "bulk_edit", path="bulk-edit", detail=False)
class PodBulkEditView(generic.BulkEditView):
    queryset = models.Pod.objects.all()
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
    form = forms.PodBulkEditForm


@register_model_view(models.Pod, "bulk_delete", path="bulk-delete", detail=False)
class PodBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Pod.objects.all()
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
