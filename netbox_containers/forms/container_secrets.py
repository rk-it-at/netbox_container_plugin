from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField

from netbox_containers.models import Container, ContainerSecret, Secret
from netbox_containers.models.container_secrets import ContainerSecretTypeChoices

__all__ = (
    "ContainerSecretCreateForm",
    "ContainerSecretEditForm",
    "ContainerSecretForm",
)


class ContainerSecretForm(NetBoxModelForm):
    container = DynamicModelChoiceField(
        queryset=Container.objects.all(), required=False
    )
    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=True)
    type = forms.ChoiceField(choices=ContainerSecretTypeChoices.choices, required=True)

    class Meta:
        model = ContainerSecret
        fields = ("container", "secret", "type", "target", "uid", "gid", "mode", "tags")

    # The uid/gid/mode-vs-ENV rule lives in ContainerSecret.clean() on the
    # model, which ModelForm._post_clean() already runs for every form below.


class ContainerSecretCreateForm(NetBoxModelForm):
    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=True)
    type = forms.ChoiceField(choices=ContainerSecretTypeChoices.choices, required=True)

    class Meta:
        model = ContainerSecret
        fields = ("secret", "type", "target", "uid", "gid", "mode", "tags")

    def __init__(self, *args, **kwargs):
        self._container_id = kwargs.pop("container_id", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self._container_id:
            obj.container_id = self._container_id
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class ContainerSecretEditForm(NetBoxModelForm):
    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=True)
    type = forms.ChoiceField(choices=ContainerSecretTypeChoices.choices, required=True)

    class Meta:
        model = ContainerSecret
        fields = ("secret", "type", "target", "uid", "gid", "mode", "tags")
