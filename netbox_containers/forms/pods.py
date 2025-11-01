from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField
from netbox_containers.models import Pod, Network
from netbox_containers.filtersets import PodFilterSet


__all__ = (
    "PodForm",
    "PodFilterForm",
)


class PodForm(NetBoxModelForm):
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks",
    )

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.fields["infra"].queryset = Container.objects.filter(isinfra=True)


class PodFilterForm(NetBoxModelFilterSetForm):
    model = Pod
    filterset_class = PodFilterSet
