from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, CommentField
from dcim.models import Device
from virtualization.models import VirtualMachine
from ipam.models import Prefix
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
    prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label='Prefixes',
        help_text='Select one or more existing IPAM prefixes (optional).'
    )
    # Accept multiple CIDRs entered as lines; we’ll normalize into JSON list
    subnets_text_input = forms.CharField(
        required=False,
        label='Subnets (text)',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': '10.10.0.0/24\n192.0.2.0/25'}),
        help_text='Enter one CIDR per line if you are not using only Prefixes.',
    )
    comments = CommentField(required=False)

    class Meta:
        model = Network
        fields = [
            "name",
            "driver",
            "user",
            "devices",
            "virtual_machines",
            'prefixes',
            'subnets_text_input',
            'label',
            'gateway',
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate textarea from existing JSON list
        if self.instance and self.instance.pk and self.instance.subnets_text:
            self.fields['subnets_text_input'].initial = '\n'.join(self.instance.subnets_text)

    def clean_subnets_text_input(self):
        # Return a normalized list from the textarea; actual CIDR validation is in model.clean()
        data = self.cleaned_data.get('subnets_text_input') or ''
        # split on newlines/commas; ignore blanks
        items = []
        for raw in (x.strip() for line in data.splitlines() for x in line.split(',')):
            if raw:
                items.append(raw)
        return items

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.subnets_text = self.cleaned_data.get('subnets_text_input', [])
        if commit:
            obj.full_clean()
            obj.save()
            self.save_m2m()
        return obj


class NetworkFilterForm(NetBoxModelFilterSetForm):
    model = Network
    filterset_class = NetworkFilterSet
