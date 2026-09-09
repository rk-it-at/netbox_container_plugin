from django.db.models import Count
from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from netbox_containers import filtersets, forms, models, tables
from netbox_containers.models.pods import PodStatusChoices
from netbox_containers.views.mixins import RelatedDeviceVMTablesMixin

__all__ = (
    "PodDeleteView",
    "PodEditView",
    "PodListView",
    "PodNetworkAttachmentListView",
    "PodView",
)


@register_model_view(models.Pod)
class PodView(RelatedDeviceVMTablesMixin, generic.ObjectView):
    queryset = models.Pod.objects.prefetch_related(
        "network_attachments__network",
    )
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
    template_name = "netbox_containers/pod.html"
    form = forms.PodForm

    def get_extra_context(self, request, instance):
        containers_table = tables.ContainerTable(
            instance.containers.annotate(
                device_count=Count("devices", distinct=True)
            ).annotate(vm_count=Count("virtual_machines", distinct=True)),
            prefix="containers-",
        )
        containers_table.configure(request)
        containers_table.columns.hide("pod")

        networks_table = tables.NetworkAttachmentTable(
            instance.network_attachments.all(), prefix="networks-"
        )
        networks_table.configure(request)
        networks_table.columns.hide("container")
        networks_table.columns.hide("pod")

        devices_table, vms_table = self.get_device_vm_tables(request, instance)
        return {
            "containers_table": containers_table,
            "networks_table": networks_table,
            "devices_table": devices_table,
            "vms_table": vms_table,
            "PodStatusChoices": PodStatusChoices,  # expose colors mapping to the template
        }


@register_model_view(models.Pod, "list", path="", detail=False)
class PodListView(generic.ObjectListView):
    queryset = (
        models.Pod.objects.annotate(container_count=Count("containers", distinct=True))
        .annotate(device_count=Count("devices", distinct=True))
        .annotate(vm_count=Count("virtual_machines", distinct=True))
    )
    table = tables.PodTable
    filterset = filtersets.PodFilterSet
    filterset_form = forms.PodFilterForm


@register_model_view(models.Pod, "add", detail=False)
@register_model_view(models.Pod, "edit")
class PodEditView(generic.ObjectEditView):
    queryset = models.Pod.objects.all()
    form = forms.PodForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        field = form.fields.get("infra_container")
        if field:
            if form.instance.pk:
                field.queryset = models.Container.objects.filter(
                    is_infra=True,
                    pod_id=form.instance.pk,
                )
            else:
                field.queryset = models.Container.objects.none()
        return form


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


@register_model_view(models.Pod, name="network_attachments", path="network-attachments")
class PodNetworkAttachmentListView(generic.ObjectChildrenView):
    """
    /plugins/netbox-containers/pods/<id>/network-attachments/
    """

    queryset = models.Pod.objects.all()

    child_model = models.NetworkAttachment
    table = tables.NetworkAttachmentTable
    template_name = "netbox_containers/network_attachment_children.html"
    tab = ViewTab(
        label="Networks",
        badge=lambda obj: obj.network_attachments.count(),
        permission="netbox_containers.view_networkattachment",
    )

    def get_children(self, request, parent):
        return self.get_children_queryset(request, parent)

    def get_children_queryset(self, request, parent):
        return (
            self.child_model.objects.filter(pod=parent)
            .select_related("network")
            .order_by("pk")
        )
