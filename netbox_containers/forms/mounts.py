from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from netbox_containers.models import Mount, Volume
from netbox_containers.models.mounts import MountTypeChoices


__all__ = (
    "MountForm",
    "MountCreateForm",
)


class MountForm(NetBoxModelForm):
    volume = DynamicModelChoiceField(queryset=Volume.objects.all(), required=False)
    mount_type = forms.ChoiceField(choices=MountTypeChoices.choices, required=True)

    fieldsets = (
        FieldSet(
            "container",
            "mount_type",
            "volume",
            "host_path",
            "dest_path",
            "options",
            "tags",
            name=_("Mount"),
        ),
    )

    class Meta:
        model = Mount
        fields = ("container", "mount_type", "volume", "host_path", "dest_path", "options")

    def clean(self):
        cleaned = self.cleaned_data
        mtype = cleaned.get("mount_type")
        vol = cleaned.get("volume")
        host = (cleaned.get("host_path") or "").strip()

        if mtype == MountTypeChoices.VOLUME:
            if not vol:
                raise forms.ValidationError("Select a volume for a volume mount.")
            if host:
                raise forms.ValidationError("Host path must be empty for volume mounts.")

        if mtype == MountTypeChoices.BIND:
            if not host:
                raise forms.ValidationError("Host path is required for bind mounts.")
            if vol:
                raise forms.ValidationError("Volume must be empty for bind mounts.")

        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MountCreateForm(MountForm):
    class Meta:
        model = Mount
        fields = ("mount_type", "volume", "host_path", "dest_path", "options", "tags")

    fieldsets = (
        FieldSet(
            "mount_type",
            "volume",
            "host_path",
            "dest_path",
            "options",
            "tags",
            name=_("Mount"),
        ),
    )

    def __init__(self, *args, **kwargs):
        self._container_id = kwargs.pop("container_id", None)
        super().__init__(*args, **kwargs)
        if not self._container_id:
            self._container_id = self.initial.get("container")

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self._container_id:
            obj.container_id = self._container_id
        if commit:
            obj.save()
            self.save_m2m()
        return obj
