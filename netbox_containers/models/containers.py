from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox_containers.constants import ContainerStatusChoices


__all__ = (
    "Container",
)


memory_limit_validator = RegexValidator(
    regex=r'^[1-9]\d*(?:[bBkKmMgG])?$',
    message="Enter a positive number optionally followed by b, k, m, or g (e.g. 512m, 1g, 1048576).",
)


class Container(NetBoxModel):
    name = models.CharField(max_length=100)
    image_tag = models.ForeignKey(
        'netbox_containers.ImageTag',
        on_delete=models.PROTECT,   # prevent deleting an ImageTag in use
        related_name='containers',
        blank=True,
        null=True,
        help_text="Image + tag to run (e.g. quay.io/keycloak/keycloak:26.4)",
    )
    status = models.CharField(
        max_length=20,
        choices=ContainerStatusChoices,
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    published_ports = models.TextField(
        blank=True,
        help_text="One mapping per line: host_port:container_port (e.g. 8080:80).",
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
    command = models.CharField(max_length=200, blank=True, null=True)
    user_namespaces = models.CharField(max_length=100, blank=True, null=True)
    memory_limit = models.CharField(
        max_length=16,
        blank=True,
        validators=[memory_limit_validator],
        help_text="Podman memory limit (number[unit]): e.g. 512m, 1g",
    )
    cpu_limit = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        help_text="CPU limit (floating point, e.g. 0.5, 1.25)",
    )
    environment = models.JSONField(
        blank=True,
        default=list,
        help_text="One entry per line: KEY=VALUE (e.g. TZ=UTC)"
    )
    add_host = models.JSONField(
        blank=True,
        default=list,
        help_text="One entry per line: HOSTNAME:IP (e.g. db:10.0.0.10)"
    )
    add_group = models.JSONField(
        blank=True,
        default=list,
        help_text="One group per line: group name or gid (maps to --add-group).",
    )
    add_device = models.JSONField(
        blank=True,
        default=list,
        help_text="One device per line (maps to --device), e.g. /dev/ttyUSB0 or /dev/sda:/dev/xvda:rwm.",
    )
    is_infra = models.BooleanField(
        default=False,
        help_text="Mark this container as the infra container for a pod.",
    )


    class Meta:
        verbose_name = "Container"
        verbose_name_plural = "Containers"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_container_status_color(self):
        return ContainerStatusChoices.colors.get(self.status)

    def get_status_color(self):
        return ContainerStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:container", args=[self.pk])
