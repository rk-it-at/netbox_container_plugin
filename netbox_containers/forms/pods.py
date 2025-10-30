from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from netbox_containers.models import Pod
from netbox_containers.filtersets import PodFilterSet


__all__ = (
    "PodForm",
    "PodFilterForm",
)


class PodForm(NetBoxModelForm):
    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.fields["infra"].queryset = Container.objects.filter(isinfra=True)


class PodFilterForm(NetBoxModelFilterSetForm):
    model = Pod
    filterset_class = PodFilterSet
