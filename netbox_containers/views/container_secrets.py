import re
from django.urls import reverse
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "ContainerSecretView",
    "ContainerSecretListView",
    "ContainerSecretAddView",
    "ContainerSecretEditView",
    "ContainerSecretDeleteView",
    "ContainerSecretCreateView",
    "ContainerSecretChildListView",
)


@register_model_view(models.ContainerSecret)
class ContainerSecretView(generic.ObjectView):
    queryset = models.ContainerSecret.objects.select_related("container", "secret")
    table = tables.ContainerSecretTable
    filterset = filtersets.ContainerSecretFilterSet
    template_name = "netbox_containers/container_secret_detail.html"


@register_model_view(models.ContainerSecret, "list", path="", detail=False)
class ContainerSecretListView(generic.ObjectListView):
    queryset = models.ContainerSecret.objects.select_related("container", "secret")
    table = tables.ContainerSecretTable
    filterset = filtersets.ContainerSecretFilterSet


@register_model_view(models.ContainerSecret, "add", detail=False)
class ContainerSecretAddView(generic.ObjectEditView):
    queryset = models.ContainerSecret.objects.all()
    form = forms.ContainerSecretForm


@register_model_view(models.ContainerSecret, "edit")
class ContainerSecretEditView(generic.ObjectEditView):
    queryset = models.ContainerSecret.objects.all()
    form = forms.ContainerSecretEditForm


@register_model_view(models.ContainerSecret, "delete")
class ContainerSecretDeleteView(generic.ObjectDeleteView):
    queryset = models.ContainerSecret.objects.all()


class ContainerSecretCreateView(generic.ObjectEditView):
    queryset = models.ContainerSecret.objects.all()
    form = forms.ContainerSecretCreateForm
    template_name = "netbox_containers/container_secret_edit.html"
    default_return_url = "plugins:netbox_containers:container"

    def _get_container_id(self, request):
        container_id = self.kwargs.get("container_id")
        if not container_id and request.resolver_match:
            container_id = request.resolver_match.kwargs.get("container_id")
        if not container_id:
            match = re.search(r"/containers/(?P<cid>\\d+)/secrets/add/?", request.path)
            if match:
                container_id = match.group("cid")
        return int(container_id) if container_id else None

    def get_object(self, queryset=None, **kwargs):
        container_id = self._get_container_id(self.request)
        return models.ContainerSecret(container_id=container_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        container_id = self._get_container_id(self.request)
        if container_id:
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


@register_model_view(models.Container, name="secrets", path="secrets")
class ContainerSecretChildListView(generic.ObjectChildrenView):
    """
    /plugins/netbox-containers/containers/<id>/secrets/
    """
    queryset = models.Container.objects.all()

    child_model = models.ContainerSecret
    table = tables.ContainerSecretTable
    template_name = "netbox_containers/container_secret_children.html"
    tab = ViewTab(
        label="Secrets",
        badge=lambda obj: obj.secrets.count(),
        permission="netbox_containers.view_containersecret",
    )

    def get_children(self, request, parent):
        return self.get_children_queryset(request, parent)

    def get_children_queryset(self, request, parent):
        return (
            self.child_model.objects
            .filter(container=parent)
            .select_related("secret")
            .order_by("pk")
        )

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("container")
        return table
