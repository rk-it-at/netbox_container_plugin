from django.db.models import Count, Q
from netbox.views import generic
from utilities.views import register_model_view

from netbox_containers import filtersets, forms, models, tables
from netbox_containers.views.mixins import RelatedDeviceVMTablesMixin

__all__ = (
    "NetworkDeleteView",
    "NetworkEditView",
    "NetworkListView",
    "NetworkView",
)


@register_model_view(models.Network)
class NetworkView(RelatedDeviceVMTablesMixin, generic.ObjectView):
    queryset = models.Network.objects.prefetch_related(
        "attachments__pod",
        "attachments__container",
    )
    table = tables.NetworkTable
    filterset = filtersets.NetworkFilterSet
    template_name = "netbox_containers/network.html"

    def get_extra_context(self, request, instance):
        pod_ids = instance.attachments.filter(pod__isnull=False).values_list(
            "pod_id", flat=True
        )
        pods_table = tables.PodTable(
            models.Pod.objects.filter(pk__in=pod_ids)
            .annotate(container_count=Count("containers", distinct=True))
            .annotate(device_count=Count("devices", distinct=True))
            .annotate(vm_count=Count("virtual_machines", distinct=True)),
            prefix="pods-",
        )
        pods_table.configure(request)

        container_ids = instance.attachments.filter(
            container__isnull=False
        ).values_list("container_id", flat=True)
        containers_table = tables.ContainerTable(
            models.Container.objects.filter(pk__in=container_ids)
            .annotate(device_count=Count("devices", distinct=True))
            .annotate(vm_count=Count("virtual_machines", distinct=True)),
            prefix="containers-",
        )
        containers_table.configure(request)

        devices_table, vms_table = self.get_device_vm_tables(request, instance)
        return {
            "pods_table": pods_table,
            "containers_table": containers_table,
            "devices_table": devices_table,
            "vms_table": vms_table,
        }


@register_model_view(models.Network, "list", path="", detail=False)
class NetworkListView(generic.ObjectListView):
    queryset = (
        models.Network.objects.annotate(
            pod_count=Count(
                "attachments__pod",
                filter=Q(attachments__pod__isnull=False),
                distinct=True,
            )
        )
        .annotate(
            container_count=Count(
                "attachments__container",
                filter=Q(attachments__container__isnull=False),
                distinct=True,
            )
        )
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
