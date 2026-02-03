import re
from django.urls import reverse
from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "MountView",
    "MountListView",
    "MountEditView",
    "MountDeleteView",
    "MountCreateView",
)


@register_model_view(models.Mount)
class MountView(generic.ObjectView):
    queryset = models.Mount.objects.select_related("container", "volume")
    table = tables.MountTable
    filterset = filtersets.MountFilterSet
    template_name = "netbox_containers/mount_detail.html"


@register_model_view(models.Mount, "list", path="", detail=False)
class MountListView(generic.ObjectListView):
    queryset = models.Mount.objects.select_related("container", "volume")
    table = tables.MountTable
    filterset = filtersets.MountFilterSet


@register_model_view(models.Mount, "add", detail=False)
@register_model_view(models.Mount, "edit")
class MountEditView(generic.ObjectEditView):
    queryset = models.Mount.objects.all()
    form = forms.MountForm


@register_model_view(models.Mount, "delete")
class MountDeleteView(generic.ObjectDeleteView):
    queryset = models.Mount.objects.all()


class MountCreateView(generic.ObjectEditView):
    queryset = models.Mount.objects.all()
    table = tables.MountTable
    filterset = filtersets.MountFilterSet
    template_name = "netbox_containers/mount.html"
    form = forms.MountCreateForm
    default_return_url = "plugins:netbox_containers:container"

    def get_object(self, queryset=None, **kwargs):
        # Return an unsaved instance so templates can access _meta.
        container_id = self._get_container_id(self.request)
        if container_id:
            return models.Mount(container_id=container_id)
        return models.Mount()

    def _get_container_id(self, request):
        container_id = self.kwargs.get("container_id")
        if not container_id and request.resolver_match:
            container_id = request.resolver_match.kwargs.get("container_id")
        if not container_id:
            container_id = request.GET.get("container_id") or request.GET.get("container")
        if not container_id:
            match = re.search(r"/containers/(?P<cid>\\d+)/mounts/add/?", request.path)
            if match:
                container_id = match.group("cid")
        return int(container_id) if container_id else None

    def get_initial(self):
        initial = super().get_initial()
        container_id = self._get_container_id(self.request)
        if container_id:
            initial["container"] = container_id
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        container_id = self._get_container_id(self.request)
        if container_id:
            kwargs.setdefault("initial", {})
            kwargs["initial"]["container"] = container_id
            kwargs["container_id"] = container_id
        return kwargs

    def form_valid(self, form):
        container_id = self._get_container_id(self.request)
        if container_id and not form.instance.container_id:
            form.instance.container_id = container_id
        return super().form_valid(form)

    def get_return_url(self, request, obj=None):
        container_id = self._get_container_id(request)
        if container_id:
            return reverse("plugins:netbox_containers:container", kwargs={"pk": container_id})
        return super().get_return_url(request, obj)
