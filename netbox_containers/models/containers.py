from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox_containers.constants import ContainerStatusChoices


__all__ = (
    "Container",
)


class Container(NetBoxModel):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=ContainerStatusChoices,
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    published_ports = models.CharField(max_length=200, blank=True, null=True)
    networks = models.ManyToManyField(
        'netbox_containers.Network',
        related_name='containers',
        blank=True,
        null=True,
    )
    pod = models.ForeignKey(
        'netbox_containers.Pod',
        on_delete=models.SET_NULL,
        related_name='containers',
        blank=True,
        null=True,
    )
    comments = models.TextField(blank=True)
    devices = models.ManyToManyField(
        "dcim.Device",
        related_name="container_containers",
        blank=True,
    )
    virtual_machines = models.ManyToManyField(
        "virtualization.VirtualMachine",
        related_name="container_containers",
        blank=True,
    )

    class Meta:
        verbose_name = "Container"
        verbose_name_plural = "Containers"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_container_status_color(self):
        return ContainerStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:container", args=[self.pk])
