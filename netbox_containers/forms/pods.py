from django import forms
import json
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Pod, Container
from netbox_containers.forms.containers import HOST_ENTRY_RE


__all__ = (
    "PodForm",
    "PodFilterForm",
    "PodBulkEditForm",
)


class PodForm(NetBoxModelForm):
    comments = CommentField(required=False)
    published_ports = forms.CharField(
        required=False,
        label="Published Ports",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One mapping per line: host_port:container_port (e.g. 8080:80).",
    )
    add_host_text = forms.CharField(
        required=False,
        label="Add hosts",
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text="One per line: hostname:ip (maps to --add-host).",
    )
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
    infra_container = DynamicModelChoiceField(
        queryset=Container.objects.none(),
        required=False,
        label="Infra container",
        query_params={
            "is_infra": "true",
        },
    )

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "infra_container",
            "add_host_text",
            "devices",
            "virtual_machines",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["infra_container"].queryset = Container.objects.filter(
                is_infra=True,
                pod=self.instance,
            )
            params = [
                {"queryParam": "is_infra", "queryValue": [True]},
                {"queryParam": "pod_id", "queryValue": [self.instance.pk]},
            ]
            self.fields["infra_container"].query_params = {
                "is_infra": "true",
                "pod_id": str(self.instance.pk),
            }
            widget = self.fields["infra_container"].widget
            widget.attrs["data-static-params"] = json.dumps(params)
            widget.attrs.pop("data-dynamic-params", None)
            self.initial["add_host_text"] = "\n".join(self.instance.add_host or [])
        else:
            self.fields["infra_container"].queryset = Container.objects.none()

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

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.add_host = self.cleaned_data.get("add_host_text", [])
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class PodBulkEditForm(NetBoxModelBulkEditForm):
    model = Pod

    user = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "user",
            name=_("Pod"),
        ),
    )

    nullable_fields = ("user", "comments")  


class PodFilterForm(NetBoxModelFilterSetForm):
    model = Pod

    q = forms.CharField(required=False, label="Search")

    status = forms.ChoiceField(
        choices=Pod._meta.get_field("status").choices,
        required=False,
        label=_("Status"),
    )
    user   = forms.CharField(required=False, label="User")

    fieldsets = (
        FieldSet("q", "status", "user", name=_("Pods")),
    )
