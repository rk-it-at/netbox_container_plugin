from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


__all__ = (
    "Network",
)


class Network(NetBoxModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:network", args=[self.pk])
