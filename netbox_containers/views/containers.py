from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets
from netbox_containers.models.containers import ContainerStatusChoices


__all__ = (
    "ContainerView",
    "ContainerListView",
    "ContainerEditView",
    "ContainerDeleteView",
)


@register_model_view(models.Container)
class ContainerView(generic.ObjectView):
    queryset = models.Container.objects.all()
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    template_name = "netbox_containers/container.html"
    form = forms.ContainerForm

    def get_extra_context(self, request, instance):
        return {
            "ContainerStatusChoices": ContainerStatusChoices,  # expose colors mapping to the template
        }


@register_model_view(models.Container, "list", path="", detail=False)
class ContainerListView(generic.ObjectListView):
    queryset = models.Container.objects.all()
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    filterset_form = forms.ContainerFilterForm


@register_model_view(models.Container, "add", detail=False)
@register_model_view(models.Container, "edit")
class ContainerEditView(generic.ObjectEditView):
    queryset = models.Container.objects.all()
    form = forms.ContainerForm


@register_model_view(models.Container, "delete")
class ContainerDeleteView(generic.ObjectDeleteView):
    queryset = models.Container.objects.all()


@register_model_view(models.Container, "bulk_edit", path="bulk-edit", detail=False)
class ContainerBulkEditView(generic.BulkEditView):
    queryset = models.Container.objects.all()
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    form = forms.ContainerBulkEditForm


@register_model_view(models.Container, "bulk_delete", path="bulk-delete", detail=False)
class ContainerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Container.objects.all()
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet


@register_model_view(models.Container, "changelog", path="changelog")
class ContainerChangeLogView(generic.ObjectChangeLogView):
    queryset = models.Container.objects.all()


@register_model_view(models.Container, "journal", path="journal")
class ContainerJournalView(generic.ObjectJournalView):
    queryset = models.Container.objects.all()
