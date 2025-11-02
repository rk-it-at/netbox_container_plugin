from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Pod, Network


__all__ = (
    "PodForm",
    "PodFilterForm",
    "PodBulkEditForm",
)


class PodForm(NetBoxModelForm):
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks",
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

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "devices",
            "virtual_machines",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

    # Filter Pods by related Networks
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks"
    )

    fieldsets = (
        FieldSet("q", "status", "user", "networks", name=_("Pods")),
    )
