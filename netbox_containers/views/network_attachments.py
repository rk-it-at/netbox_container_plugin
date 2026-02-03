import re
from django.urls import reverse
from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "NetworkAttachmentView",
    "NetworkAttachmentListView",
    "NetworkAttachmentContainerListView",
    "NetworkAttachmentPodListView",
    "NetworkAttachmentAddView",
    "NetworkAttachmentEditView",
    "NetworkAttachmentDeleteView",
    "NetworkAttachmentCreateView",
)


@register_model_view(models.NetworkAttachment)
class NetworkAttachmentView(generic.ObjectView):
    queryset = models.NetworkAttachment.objects.select_related("network", "container", "pod")
    table = tables.NetworkAttachmentTable
    filterset = filtersets.NetworkAttachmentFilterSet
    template_name = "netbox_containers/network_attachment_detail.html"


@register_model_view(models.NetworkAttachment, "list", path="", detail=False)
class NetworkAttachmentListView(generic.ObjectListView):
    queryset = models.NetworkAttachment.objects.select_related("network", "container", "pod")
    table = tables.NetworkAttachmentTable
    filterset = filtersets.NetworkAttachmentFilterSet


class NetworkAttachmentContainerListView(generic.ObjectListView):
    queryset = models.NetworkAttachment.objects.filter(container__isnull=False).select_related("network", "container")
    table = tables.NetworkAttachmentTable
    filterset = filtersets.NetworkAttachmentFilterSet

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("pod")
        return table


class NetworkAttachmentPodListView(generic.ObjectListView):
    queryset = models.NetworkAttachment.objects.filter(pod__isnull=False).select_related("network", "pod")
    table = tables.NetworkAttachmentTable
    filterset = filtersets.NetworkAttachmentFilterSet

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("container")
        return table


@register_model_view(models.NetworkAttachment, "edit")
class NetworkAttachmentEditView(generic.ObjectEditView):
    queryset = models.NetworkAttachment.objects.all()
    form = forms.NetworkAttachmentEditForm


@register_model_view(models.NetworkAttachment, "delete")
class NetworkAttachmentDeleteView(generic.ObjectDeleteView):
    queryset = models.NetworkAttachment.objects.all()


@register_model_view(models.NetworkAttachment, "add", detail=False)
class NetworkAttachmentAddView(generic.ObjectEditView):
    queryset = models.NetworkAttachment.objects.all()
    form = forms.NetworkAttachmentForm


class NetworkAttachmentCreateView(generic.ObjectEditView):
    queryset = models.NetworkAttachment.objects.all()
    form = forms.NetworkAttachmentCreateForm
    template_name = "netbox_containers/network_attachment_edit.html"
    default_return_url = "plugins:netbox_containers:container"

    def _get_container_id(self, request):
        container_id = self.kwargs.get("container_id")
        if not container_id and request.resolver_match:
            container_id = request.resolver_match.kwargs.get("container_id")
        if not container_id:
            match = re.search(r"/containers/(?P<cid>\\d+)/network-attachments/add/?", request.path)
            if match:
                container_id = match.group("cid")
        return int(container_id) if container_id else None

    def _get_pod_id(self, request):
        pod_id = self.kwargs.get("pod_id")
        if not pod_id and request.resolver_match:
            pod_id = request.resolver_match.kwargs.get("pod_id")
        if not pod_id:
            match = re.search(r"/pods/(?P<pid>\\d+)/network-attachments/add/?", request.path)
            if match:
                pod_id = match.group("pid")
        return int(pod_id) if pod_id else None

    def get_object(self, queryset=None, **kwargs):
        container_id = self._get_container_id(self.request)
        pod_id = self._get_pod_id(self.request)
        return models.NetworkAttachment(container_id=container_id, pod_id=pod_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        container_id = self._get_container_id(self.request)
        pod_id = self._get_pod_id(self.request)
        if container_id:
            kwargs["container_id"] = container_id
        if pod_id:
            kwargs["pod_id"] = pod_id
        return kwargs

    def form_valid(self, form):
        container_id = self._get_container_id(self.request)
        pod_id = self._get_pod_id(self.request)
        if container_id and not form.instance.container_id:
            form.instance.container_id = container_id
        if pod_id and not form.instance.pod_id:
            form.instance.pod_id = pod_id
        return super().form_valid(form)

    def get_return_url(self, request, obj=None):
        container_id = self._get_container_id(request)
        if container_id:
            return reverse("plugins:netbox_containers:container", kwargs={"pk": container_id})
        pod_id = self._get_pod_id(request)
        if pod_id:
            return reverse("plugins:netbox_containers:pod", kwargs={"pk": pod_id})
        return super().get_return_url(request, obj)
