from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox_containers.constants import VolumeDriverChoices


__all__ = (
    "Volume",
)


class Volume(NetBoxModel):
    name = models.CharField(max_length=100)
    driver = models.CharField(
        max_length=20,
        choices=VolumeDriverChoices,
    )
    options = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "Volume"
        verbose_name_plural = "Volumes"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_volume_driver_color(self):
        return VolumeDriverChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:volume", args=[self.pk])
