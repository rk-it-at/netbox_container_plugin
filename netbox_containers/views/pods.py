from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "PodView",
    "PodListView",
    "PodEditView",
    "PodDeleteView",
)


@register_model_view(models.Pod)
class PodView(generic.ObjectView):
    queryset = models.Pod.objects.all()


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
