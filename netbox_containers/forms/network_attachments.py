from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from netbox_containers.models import NetworkAttachment, Network, Pod, Container
from netbox_containers.models.network_attachments import NetworkAttachmentModeChoices


__all__ = (
    "NetworkAttachmentForm",
    "NetworkAttachmentCreateForm",
    "NetworkAttachmentEditForm",
)


class NetworkAttachmentForm(NetBoxModelForm):
    container = DynamicModelChoiceField(queryset=Container.objects.all(), required=False)
    pod = DynamicModelChoiceField(queryset=Pod.objects.all(), required=False)
    network = DynamicModelChoiceField(queryset=Network.objects.all(), required=False)
    mode = forms.ChoiceField(choices=NetworkAttachmentModeChoices.choices, required=True)

    class Meta:
        model = NetworkAttachment
        fields = ("container", "pod", "mode", "network", "options", "tags")

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        container = cleaned.get("container")
        pod = cleaned.get("pod")
        mode = cleaned.get("mode")
        network = cleaned.get("network")
        options = (cleaned.get("options") or "").strip()

        if "container" in self.fields or "pod" in self.fields:
            if bool(container) == bool(pod):
                raise forms.ValidationError("Select either a container or a pod.")
        else:
            if bool(self.instance.container_id) == bool(self.instance.pod_id):
                raise forms.ValidationError("Select either a container or a pod.")

        if mode == NetworkAttachmentModeChoices.NETWORK:
            if not network:
                raise forms.ValidationError("Select a network for network mode.")
            if options:
                raise forms.ValidationError("Options must be empty for network mode.")

        if mode == NetworkAttachmentModeChoices.CUSTOM:
            if not options:
                raise forms.ValidationError("Options must be set for options mode.")
            if network:
                raise forms.ValidationError("Network must be empty for options mode.")

        if mode in (NetworkAttachmentModeChoices.NONE, NetworkAttachmentModeChoices.HOST, NetworkAttachmentModeChoices.PRIVATE):
            if network:
                raise forms.ValidationError("Network must be empty for this mode.")
            if options:
                raise forms.ValidationError("Options must be empty for this mode.")

        return cleaned


class NetworkAttachmentCreateForm(NetBoxModelForm):
    network = DynamicModelChoiceField(queryset=Network.objects.all(), required=False)
    mode = forms.ChoiceField(choices=NetworkAttachmentModeChoices.choices, required=True)

    class Meta:
        model = NetworkAttachment
        fields = ("mode", "network", "options", "tags")

    def __init__(self, *args, **kwargs):
        self._container_id = kwargs.pop("container_id", None)
        self._pod_id = kwargs.pop("pod_id", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        mode = cleaned.get("mode")
        network = cleaned.get("network")
        options = (cleaned.get("options") or "").strip()

        if mode == NetworkAttachmentModeChoices.NETWORK:
            if not network:
                raise forms.ValidationError("Select a network for network mode.")
            if options:
                raise forms.ValidationError("Options must be empty for network mode.")

        if mode == NetworkAttachmentModeChoices.CUSTOM:
            if not options:
                raise forms.ValidationError("Options must be set for options mode.")
            if network:
                raise forms.ValidationError("Network must be empty for options mode.")

        if mode in (NetworkAttachmentModeChoices.NONE, NetworkAttachmentModeChoices.HOST, NetworkAttachmentModeChoices.PRIVATE):
            if network:
                raise forms.ValidationError("Network must be empty for this mode.")
            if options:
                raise forms.ValidationError("Options must be empty for this mode.")

        return cleaned

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

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        mode = cleaned.get("mode")
        network = cleaned.get("network")
        options = (cleaned.get("options") or "").strip()

        if mode == NetworkAttachmentModeChoices.NETWORK:
            if not network:
                raise forms.ValidationError("Select a network for network mode.")
            if options:
                raise forms.ValidationError("Options must be empty for network mode.")

        if mode == NetworkAttachmentModeChoices.CUSTOM:
            if not options:
                raise forms.ValidationError("Options must be set for options mode.")
            if network:
                raise forms.ValidationError("Network must be empty for options mode.")

        if mode in (NetworkAttachmentModeChoices.NONE, NetworkAttachmentModeChoices.HOST, NetworkAttachmentModeChoices.PRIVATE):
            if network:
                raise forms.ValidationError("Network must be empty for this mode.")
            if options:
                raise forms.ValidationError("Options must be empty for this mode.")

        return cleaned
