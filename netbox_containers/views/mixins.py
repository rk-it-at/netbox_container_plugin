import re

from dcim.tables import DeviceTable
from virtualization.tables import VirtualMachineTable

__all__ = (
    "ParentLookupMixin",
    "RelatedDeviceVMTablesMixin",
)


class ParentLookupMixin:
    """Shared helper for "add a child object from a parent's detail page" views.

    Container/Pod ids can arrive as a captured URL kwarg, in the resolver match
    (when the view is instantiated outside the normal URL dispatch, e.g. in
    tests), as a query parameter, or - as a last resort - by matching the raw
    request path. Views mix this in and expose one small wrapper per parent id
    they care about instead of repeating the whole lookup chain.
    """

    def _get_parent_id(self, request, kwarg_name, path_regex, get_param_names=()):
        value = self.kwargs.get(kwarg_name)
        if not value and request.resolver_match:
            value = request.resolver_match.kwargs.get(kwarg_name)
        for get_param in [] if value else list(get_param_names):
            value = request.GET.get(get_param)
            if value:
                break
        if not value:
            match = re.search(path_regex, request.path)
            if match:
                value = match.group("id")
        return int(value) if value else None


class RelatedDeviceVMTablesMixin:
    """Builds ready-to-render tables for a model's devices/virtual_machines M2M."""

    def get_device_vm_tables(self, request, instance):
        devices_table = DeviceTable(instance.devices.all(), prefix="devices-")
        devices_table.configure(request)
        devices_table.columns.hide("pk")

        vms_table = VirtualMachineTable(instance.virtual_machines.all(), prefix="vms-")
        vms_table.configure(request)
        vms_table.columns.hide("pk")

        return devices_table, vms_table
