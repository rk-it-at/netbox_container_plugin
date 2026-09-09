from dcim.models import Device
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
)
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet
from virtualization.models import VirtualMachine

from netbox_containers.forms.fields import (
    DEVICE_ENTRY_RE,
    ENV_ENTRY_RE,
    GROUP_ENTRY_RE,
    HOST_ENTRY_RE,
    LineListField,
)
from netbox_containers.models import Container, Image, ImageTag, Pod

__all__ = (
    "ContainerBulkEditForm",
    "ContainerFilterForm",
    "ContainerForm",
)


memory_limit_validator = RegexValidator(
    regex=r"^[1-9]\d*(?:[bBkKmMgG])?$",
    message="Enter a positive number optionally followed by b, k, m, or g (e.g. 512m, 1g, 1048576).",
)


class ContainerForm(NetBoxModelForm):
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )
    published_ports = forms.CharField(
        required=False,
        label="Published Ports",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One mapping per line: host_port:container_port (e.g. 8080:80).",
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
    add_host_text = LineListField(
        label="Add hosts",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: hostname:ip (maps to --add-host).",
        line_regex=HOST_ENTRY_RE,
        line_error="Invalid add-host entry. Use one per line in the form "
        "hostname:ip. Bad entries: {bad}",
    )
    add_group_text = LineListField(
        label="Add groups",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: group name or gid (maps to --add-group).",
        line_regex=GROUP_ENTRY_RE,
        line_error="Invalid add-group entry. Use one group name or gid per "
        "line. Bad entries: {bad}",
    )
    add_device_text = LineListField(
        label="Add devices",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: /dev/... (maps to --device), e.g. /dev/ttyUSB0 or /dev/sda:/dev/xvda:rwm.",
        line_regex=DEVICE_ENTRY_RE,
        line_error="Invalid add-device entry. Use one /dev/... entry per "
        "line. Bad entries: {bad}",
    )
    environment_text = LineListField(
        label="Environment variables",
        widget=forms.Textarea(attrs={"rows": 6}),
        help_text="One per line: KEY=VALUE (maps to --env).",
        line_regex=ENV_ENTRY_RE,
        line_error="Invalid env entry. Use one per line in the form "
        "KEY=VALUE. Bad entries: {bad}",
    )

    class Meta:
        model = Container
        fields = (
            "name",
            "status",
            "user",
            "published_ports",
            "pod",
            "is_infra",
            "image",
            "image_tag",
            "command",
            "user_namespaces",
            "memory_limit",
            "cpu_limit",
            "environment_text",
            "add_host_text",
            "add_group_text",
            "add_device_text",
            "devices",
            "virtual_machines",
            "tags",
            "comments",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image_tag"].queryset = ImageTag.objects.none()

        if self.instance.pk:
            self.initial["add_host_text"] = self.instance.add_host
            self.initial["add_group_text"] = self.instance.add_group
            self.initial["add_device_text"] = self.instance.add_device
            self.initial["environment_text"] = self.instance.environment

        # Editing existing container → prepopulate
        if self.instance.pk and self.instance.image_tag:
            self.fields["image"].initial = self.instance.image_tag.image
            self.fields["image_tag"].queryset = ImageTag.objects.filter(
                image=self.instance.image_tag.image
            )

        # Image selected (POST)
        if "image" in self.data:
            try:
                image_id = int(self.data.get("image"))
                self.fields["image_tag"].queryset = ImageTag.objects.filter(
                    image_id=image_id
                )
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.image_tag_id:
            self.fields["image_tag"].queryset = ImageTag.objects.filter(
                image=self.instance.image_tag.image
            )

    def clean(self):
        super().clean()

        image = self.cleaned_data.get("image")
        image_tag = self.cleaned_data.get("image_tag")

        if image_tag and image and image_tag.image != image:
            raise forms.ValidationError(
                "Selected tag does not belong to selected image."
            )

        return self.cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.add_host = self.cleaned_data.get("add_host_text", [])
        obj.add_group = self.cleaned_data.get("add_group_text", [])
        obj.add_device = self.cleaned_data.get("add_device_text", [])
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
    user = forms.CharField(required=False, label="User")

    # Filter Containers by related Networks
    pod = DynamicModelChoiceField(
        queryset=Pod.objects.all(),
        required=False,
        label="Pod",
    )

    fieldsets = (FieldSet("q", "status", "user", "pod", name=_("Containers")),)
