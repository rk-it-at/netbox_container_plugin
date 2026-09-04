from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_containers.models import Container, Network, NetworkAttachment, Pod
from netbox_containers.models.network_attachments import NetworkAttachmentModeChoices

__all__ = (
    "NetworkAttachmentCreateForm",
    "NetworkAttachmentEditForm",
    "NetworkAttachmentForm",
)


class NetworkAttachmentForm(NetBoxModelForm):
    container = DynamicModelChoiceField(
        queryset=Container.objects.all(), required=False
    )
    pod = DynamicModelChoiceField(queryset=Pod.objects.all(), required=False)
    network = DynamicModelChoiceField(queryset=Network.objects.all(), required=False)
    mode = forms.ChoiceField(
        choices=NetworkAttachmentModeChoices.choices, required=True
    )

    class Meta:
        model = NetworkAttachment
        fields = ("container", "pod", "mode", "network", "options", "tags")

    # Mode/container/pod rules live in NetworkAttachment.clean() on the model,
    # which ModelForm._post_clean() already runs for every form below.


class NetworkAttachmentCreateForm(NetBoxModelForm):
    network = DynamicModelChoiceField(queryset=Network.objects.all(), required=False)
    mode = forms.ChoiceField(
        choices=NetworkAttachmentModeChoices.choices, required=True
    )

    class Meta:
        model = NetworkAttachment
        fields = ("mode", "network", "options", "tags")

    def __init__(self, *args, **kwargs):
        self._container_id = kwargs.pop("container_id", None)
        self._pod_id = kwargs.pop("pod_id", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self._container_id:
            obj.container_id = self._container_id
        if self._pod_id:
            obj.pod_id = self._pod_id
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class NetworkAttachmentEditForm(NetworkAttachmentForm):
    class Meta:
        model = NetworkAttachment
        fields = ("mode", "network", "options", "tags")

    fieldsets = (
        FieldSet(
            "mode",
            "network",
            "options",
            "tags",
            name="Network Attachment",
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("container", None)
        self.fields.pop("pod", None)
