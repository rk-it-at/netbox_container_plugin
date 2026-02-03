from netbox.views import generic
from utilities.views import register_model_view
from netbox_containers import forms, models, tables, filtersets


__all__ = (
    "SecretView",
    "SecretListView",
    "SecretEditView",
    "SecretDeleteView",
)


@register_model_view(models.Secret)
class SecretView(generic.ObjectView):
    queryset = models.Secret.objects.all()
    table = tables.SecretTable
    filterset = filtersets.SecretFilterSet
    template_name = "netbox_containers/secret.html"


@register_model_view(models.Secret, "list", path="", detail=False)
class SecretListView(generic.ObjectListView):
    queryset = models.Secret.objects.all()
    table = tables.SecretTable
    filterset = filtersets.SecretFilterSet
    filterset_form = forms.SecretFilterForm


@register_model_view(models.Secret, "add", detail=False)
@register_model_view(models.Secret, "edit")
class SecretEditView(generic.ObjectEditView):
    queryset = models.Secret.objects.all()
    form = forms.SecretForm


@register_model_view(models.Secret, "delete")
class SecretDeleteView(generic.ObjectDeleteView):
    queryset = models.Secret.objects.all()
