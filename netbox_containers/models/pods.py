from django.db import models
from django.urls import reverse
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel
from netbox_containers import constants
from netbox_containers.constants import DEFAULT_POD_STATUSES
from netbox_containers.utils import get_plugin_config


__all__ = (
    "Pod",
    "PodStatusChoices"
)


class PodStatusChoices(ChoiceSet):
    key = "Pod.status"
    CHOICES = get_plugin_config("POD_STATUSES", DEFAULT_POD_STATUSES) or []

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


class Pod(NetBoxModel):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=PodStatusChoices,
        default=PodStatusChoices.CHOICES[0][0],
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

    class Meta:
        verbose_name = "Pod"
        verbose_name_plural = "Pods"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:pod", args=[self.pk])
