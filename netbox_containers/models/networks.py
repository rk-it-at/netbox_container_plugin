from django.db import models
from django.urls import reverse
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from netbox_containers import constants
from netbox_containers.constants import DEFAULT_NETWORK_DRIVERS
from netbox_containers.utils import get_plugin_config


__all__ = (
    "Network",
    "NetworkDriverChoices"
)


class NetworkDriverChoices(ChoiceSet):
    key = "Network.status"
    CHOICES = get_plugin_config("NETWORK_DRIVERS", DEFAULT_NETWORK_DRIVERS) or []

    COLORS = {}
    for choice in CHOICES:
        if len(choice) == 3:
            key, _, color = choice
        elif len(choice) == 2:
            key, _ = choice
            color = "gray"
        else:
            continue
        COLORS[key] = color


class Network(NetBoxModel):
    name = models.CharField(max_length=100)
    driver = models.CharField(
        max_length=20,
        choices=NetworkDriverChoices,
        default=NetworkDriverChoices.CHOICES[0][0],
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    subnet = models.CharField(max_length=200, blank=True, null=True)
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


    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"
        ordering = ("name", "pk")


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:network", args=[self.pk])
