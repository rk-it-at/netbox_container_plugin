from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Container, Pod, Network, Image, ImageTag, Volume
import re


__all__ = (
    "ContainerForm",
    "ContainerFilterForm",
    "ContainerBulkEditForm",
)


memory_limit_validator = RegexValidator(
    regex=r'^[1-9]\d*(?:[bBkKmMgG])?$',
    message="Enter a positive number optionally followed by b, k, m, or g (e.g. 512m, 1g, 1048576).",
)

HOST_ENTRY_RE = re.compile(r"^[^:\s]+:[^:\s]+$")     # hostname:ip (simple)
ENV_ENTRY_RE  = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")  # KEY=VALUE


class ContainerForm(NetBoxModelForm):
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks",
    )
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )
    comments = CommentField(required=False)
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Devices",
    )
    virtual_machines = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual machines",
    )
    image = DynamicModelChoiceField(
        queryset=Image.objects.all(),
        required=False,
        label="Image",
        help_text="Select repository/image first",
    )
    image_tag = DynamicModelChoiceField(
        queryset=ImageTag.objects.select_related("image"),
        required=False,
        label="Tag",
        help_text="Select tag (filtered by image)",
        query_params={
            "image_id": "$image",
        },
    )
    volumes = DynamicModelMultipleChoiceField(
        queryset=Volume.objects.all(),
        required=False,
        label="Volumes",
    )
    add_host_text = forms.CharField(
        required=False,
        label="Add hosts",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: hostname:ip (maps to --add-host).",
    )
    environment_text = forms.CharField(
        required=False,
        label="Environment variables",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="One per line: KEY=VALUE (maps to --env).",
    )

    class Meta:
        model = Container
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "pod",
            "image",
            "image_tag",
            "command",
            "volumes",
            "user_namespaces",
            "memory_limit",
            "cpu_limit",
            "environment_text",
            "add_host_text",
            "devices",
            "virtual_machines",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image_tag"].queryset = ImageTag.objects.none()

        if self.instance.pk:
            self.initial["add_host_text"] = "\n".join(self.instance.add_host or [])
            self.initial["environment_text"] = "\n".join(self.instance.environment or [])

        # Editing existing container → prepopulate
        if self.instance.pk and self.instance.image_tag:
            self.fields['image'].initial = self.instance.image_tag.image
            self.fields['image_tag'].queryset = ImageTag.objects.filter(
                image=self.instance.image_tag.image
            )

        # Image selected (POST)
        if 'image' in self.data:
            try:
                image_id = int(self.data.get('image'))
                self.fields['image_tag'].queryset = ImageTag.objects.filter(image_id=image_id)
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.image_tag_id:
            self.fields["image_tag"].queryset = ImageTag.objects.filter(image=self.instance.image_tag.image)

    def clean_add_host_text(self):
        raw = (self.cleaned_data.get("add_host_text") or "").strip()
        if not raw:
            return []

        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        bad = [l for l in lines if not HOST_ENTRY_RE.match(l)]
        if bad:
            raise ValidationError(
                "Invalid add-host entry. Use one per line in the form hostname:ip. "
                f"Bad entries: {', '.join(bad[:5])}"
            )
        return lines

    def clean_environment_text(self):
        raw = (self.cleaned_data.get("environment_text") or "").strip()
        if not raw:
            return []

        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        bad = [l for l in lines if not ENV_ENTRY_RE.match(l)]
        if bad:
            raise ValidationError(
                "Invalid env entry. Use one per line in the form KEY=VALUE. "
                f"Bad entries: {', '.join(bad[:5])}"
            )
        return lines

    def clean(self):
        super().clean()

        image = self.cleaned_data.get('image')
        image_tag = self.cleaned_data.get('image_tag')

        if image_tag and image and image_tag.image != image:
            raise forms.ValidationError("Selected tag does not belong to selected image.")

        return self.cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.add_host = self.cleaned_data.get("add_host_text", [])
        obj.environment = self.cleaned_data.get("environment_text", [])
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class ContainerBulkEditForm(NetBoxModelBulkEditForm):
    model = Container

    user = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "user",
            name=_("Pod"),
        ),
    )

    nullable_fields = ("user", "comments")  


class ContainerFilterForm(NetBoxModelFilterSetForm):
    model = Container

    q = forms.CharField(required=False, label="Search")

    status = forms.ChoiceField(
        choices=Container._meta.get_field("status").choices,
        required=False,
        label=_("Status"),
    )
    user   = forms.CharField(required=False, label="User")

    # Filter Containers by related Networks
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks"
    )
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )

    fieldsets = (
        FieldSet("q", "status", "user", "networks", "pod", name=_("Containers")),
    )
