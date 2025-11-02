from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from utilities.choices import ChoiceSet
from ipaddress import ip_network
from netbox.models import NetBoxModel
from netbox_containers.constants import NetworkDriverChoices


__all__ = (
    "Network",
)


class Network(NetBoxModel):
    name = models.CharField(max_length=100)
    driver = models.CharField(
        max_length=20,
        choices=NetworkDriverChoices,
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    devices = models.ManyToManyField(
        "dcim.Device",
        related_name="container_networks",
        blank=True,
    )
    virtual_machines = models.ManyToManyField(
        "virtualization.VirtualMachine",
        related_name="container_networks",
        blank=True,
    )
    prefixes = models.ManyToManyField(
        'ipam.Prefix',
        related_name='container_networks',
        blank=True,
    )
    subnets_text = models.JSONField(default=list, blank=True)
    label = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    gateway = models.GenericIPAddressField(
        protocol="both",
        blank=True,
        null=True
    )
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"
        ordering = ("name", "pk")

    def clean(self):
        super().clean()

        # Normalize and validate subnets_text to canonical CIDR strings
        if self.subnets_text is None:
            self.subnets_text = []

        if not isinstance(self.subnets_text, list):
            raise ValidationError({'subnets_text': 'Must be a list of CIDR strings or left empty.'})

        normalized = []
        for item in self.subnets_text:
            s = (item or '').strip()
            if not s:
                continue
            try:
                normalized.append(str(ip_network(s, strict=False)))
            except ValueError:
                raise ValidationError({'subnets_text': f'Invalid CIDR: {item!r}'})
        self.subnets_text = normalized

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:network", args=[self.pk])

    @property
    def effective_subnets(self):
        """List of strings; Prefixes first (as CIDR), then free-text CIDRs."""
        pref = [str(p.prefix) for p in self.prefixes.all()]
        return pref + list(self.subnets_text or [])
