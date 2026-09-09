from dcim.models import Device
from django.db.models import Count
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from virtualization.models import VirtualMachine

from netbox_containers import filtersets, forms, tables
from netbox_containers.models import Container

__all__ = (
    "DeviceContainersView",
    "VirtualMachineContainersView",
)


def _annotate_counts(queryset):
    return queryset.annotate(device_count=Count("devices", distinct=True)).annotate(
        vm_count=Count("virtual_machines", distinct=True)
    )


@register_model_view(Device, "containers")
class DeviceContainersView(generic.ObjectChildrenView):
    """
    /dcim/devices/<id>/containers/ - same idea as NetBox's own Device > Virtual
    Machines tab: only shown when a Container is actually assigned to this Device.
    """

    queryset = Device.objects.all()
    child_model = Container
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    filterset_form = forms.ContainerFilterForm
    tab = ViewTab(
        label="Containers",
        badge=lambda obj: obj.container_containers.count(),
        hide_if_empty=True,
        permission="netbox_containers.view_container",
    )

    def get_children(self, request, parent):
        qs = self.child_model.objects.restrict(request.user, "view").filter(
            devices=parent
        )
        return _annotate_counts(qs)


@register_model_view(VirtualMachine, "containers")
class VirtualMachineContainersView(generic.ObjectChildrenView):
    """
    /virtualization/virtual-machines/<id>/containers/
    """

    queryset = VirtualMachine.objects.all()
    child_model = Container
    table = tables.ContainerTable
    filterset = filtersets.ContainerFilterSet
    filterset_form = forms.ContainerFilterForm
    tab = ViewTab(
        label="Containers",
        badge=lambda obj: obj.container_containers.count(),
        hide_if_empty=True,
        permission="netbox_containers.view_container",
    )

    def get_children(self, request, parent):
        qs = self.child_model.objects.restrict(request.user, "view").filter(
            virtual_machines=parent
        )
        return _annotate_counts(qs)
