from django.core.exceptions import ValidationError
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
    infra_container = models.ForeignKey(
        "netbox_containers.Container",
        on_delete=models.SET_NULL,
        related_name="infra_for_pods",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Pod"
        verbose_name_plural = "Pods"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.infra_container:
            if not self.infra_container.is_infra:
                raise ValidationError({"infra_container": "Selected container is not marked as infra."})
            if self.infra_container.pod_id != self.pk and self.infra_container.pod_id is not None:
                raise ValidationError({"infra_container": "Infra container must belong to this pod."})

    def get_pod_status_color(self):
        return PodStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:pod", args=[self.pk])
