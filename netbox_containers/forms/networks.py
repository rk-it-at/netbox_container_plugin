from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField
from dcim.models import Device
from virtualization.models import VirtualMachine
from netbox_containers.models import Network
from netbox_containers.filtersets import NetworkFilterSet


__all__ = (
    "NetworkForm",
    "NetworkFilterForm",
)


class NetworkForm(NetBoxModelForm):
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
        model = Network
        fields = [
            "name",
            "driver",
            "user",
            "subnet",
            "devices",
            "virtual_machines",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.fields["infra"].queryset = Container.objects.filter(isinfra=True)


class NetworkFilterForm(NetBoxModelFilterSetForm):
    model = Network
    filterset_class = NetworkFilterSet
