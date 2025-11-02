from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox_containers.constants import PodStatusChoices


__all__ = (
    "Pod",
)


class Pod(NetBoxModel):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=PodStatusChoices,
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    published_ports = models.CharField(max_length=200, blank=True, null=True)
    networks = models.ManyToManyField(
        'netbox_containers.Network',
        related_name='pods',
        blank=True,
        null=True,
    )
    comments = models.TextField(blank=True)
    devices = models.ManyToManyField(
        "dcim.Device",
        related_name="container_pods",
        blank=True,
    )
    virtual_machines = models.ManyToManyField(
        "virtualization.VirtualMachine",
        related_name="container_pods",
        blank=True,
    )

    class Meta:
        verbose_name = "Pod"
        verbose_name_plural = "Pods"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_pod_status_color(self):
        return PodStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:pod", args=[self.pk])
