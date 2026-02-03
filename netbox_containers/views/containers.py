from django.db.models import Count
from django.urls import reverse
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from netbox_containers import forms, models, tables, filtersets
from netbox_containers.models.containers import ContainerStatusChoices
from netbox_containers.tables.mounts import MountTable
from netbox_containers.tables.container_secrets import ContainerSecretTable


__all__ = (
    "ContainerView",
    "ContainerListView",
    "ContainerEditView",
    "ContainerDeleteView",
    "ContainerNetworkAttachmentListView",
)


@register_model_view(models.Container)
class ContainerView(generic.ObjectView):
    queryset = models.Container.objects.prefetch_related(
        "mounts__volume",
        "network_attachments__network",
        "tags",
    )
#    queryset = models.Container.objects.all()
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    template_name = "netbox_containers/container.html"
    form = forms.ContainerForm

    # Mounts tab
    def get_children(self, request, instance):
        return [
            {
                "label": "Mounts",
                "name": "mounts",
                "icon": "mdi-database-plus",
                "permission": "netbox_containers.add_mount",
                "permissions": ["netbox_containers.add_mount"],
                "url": reverse(
                    "plugins:netbox_containers:mount_add_from_container",
                    kwargs={"container_id": instance.pk},
                ),
            },
            {
                "label": "Secrets",
                "name": "secrets",
                "icon": "mdi-key-variant",
                "permission": "netbox_containers.add_containersecret",
                "permissions": ["netbox_containers.add_containersecret"],
                "url": reverse(
                    "plugins:netbox_containers:containersecret_add_from_container",
                    kwargs={"container_id": instance.pk},
                ),
            },
        ]

    def get_extra_context(self, request, instance):
        mounts = instance.mounts.all()
        mounts_table = MountTable(mounts)
        mounts_table.configure(request)
        secrets_table = ContainerSecretTable(instance.secrets.all())
        secrets_table.configure(request)

        return {
            "mounts_table": mounts_table,
            "secrets_table": secrets_table,
            "ContainerStatusChoices": ContainerStatusChoices,  # expose colors mapping to the template
        }


@register_model_view(models.Container, "list", path="", detail=False)
class ContainerListView(generic.ObjectListView):
    queryset = (
        models.Container.objects
        .annotate(device_count=Count("devices", distinct=True))
        .annotate(vm_count=Count("virtual_machines", distinct=True))
    )
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


@register_model_view(models.Container, name="mounts", path="mounts")
class MountListView(generic.ObjectChildrenView):
    """
    /plugins/netbox-containers/containers/<id>/mounts/
    """
    queryset = models.Container.objects.all()

    child_model = models.Mount
    table = MountTable
    template_name = "netbox_containers/mount_children.html"
    tab = ViewTab(
        label="Mounts",
        badge=lambda obj: obj.mounts.count(),
        permission="netbox_containers.view_mount",
    )

    def get_children(self, request, parent):
        return self.get_children_queryset(request, parent)

    def get_children_queryset(self, request, parent):
        return (
            self.child_model.objects
            .filter(container=parent)
            .select_related("volume")
            .order_by("pk")
        )


@register_model_view(models.Container, name="network_attachments", path="network-attachments")
class ContainerNetworkAttachmentListView(generic.ObjectChildrenView):
    """
    /plugins/netbox-containers/containers/<id>/network-attachments/
    """
    queryset = models.Container.objects.all()

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
            self.child_model.objects
            .filter(container=parent)
            .select_related("network")
            .order_by("pk")
        )
