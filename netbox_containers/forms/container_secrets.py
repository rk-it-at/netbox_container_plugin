from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from netbox_containers.models import ContainerSecret, Secret, Container
from netbox_containers.models.container_secrets import ContainerSecretTypeChoices


__all__ = (
    "ContainerSecretForm",
    "ContainerSecretCreateForm",
    "ContainerSecretEditForm",
)


class ContainerSecretForm(NetBoxModelForm):
    container = DynamicModelChoiceField(queryset=Container.objects.all(), required=False)
    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=True)
    type = forms.ChoiceField(choices=ContainerSecretTypeChoices.choices, required=True)

    class Meta:
        model = ContainerSecret
        fields = ("container", "secret", "type", "target", "uid", "gid", "mode", "tags")

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        ctype = cleaned.get("type")
        uid = cleaned.get("uid")
        gid = cleaned.get("gid")
        mode = (cleaned.get("mode") or "").strip()
        if ctype == ContainerSecretTypeChoices.ENV:
            if uid or gid or mode:
                raise forms.ValidationError("UID/GID/Mode are only valid for mount secrets.")
        return cleaned


class ContainerSecretCreateForm(NetBoxModelForm):
    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=True)
    type = forms.ChoiceField(choices=ContainerSecretTypeChoices.choices, required=True)

    class Meta:
        model = ContainerSecret
        fields = ("secret", "type", "target", "uid", "gid", "mode", "tags")

    def __init__(self, *args, **kwargs):
        self._container_id = kwargs.pop("container_id", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        ctype = cleaned.get("type")
        uid = cleaned.get("uid")
        gid = cleaned.get("gid")
        mode = (cleaned.get("mode") or "").strip()
        if ctype == ContainerSecretTypeChoices.ENV:
            if uid or gid or mode:
                raise forms.ValidationError("UID/GID/Mode are only valid for mount secrets.")
        return cleaned

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

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        ctype = cleaned.get("type")
        uid = cleaned.get("uid")
        gid = cleaned.get("gid")
        mode = (cleaned.get("mode") or "").strip()
        if ctype == ContainerSecretTypeChoices.ENV:
            if uid or gid or mode:
                raise forms.ValidationError("UID/GID/Mode are only valid for mount secrets.")
        return cleaned
