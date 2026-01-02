from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Container, Pod, Network


__all__ = (
    "ContainerForm",
    "ContainerFilterForm",
    "ContainerBulkEditForm",
)


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

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "pod",
            "devices",
            "virtual_machines",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
