from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


__all__ = (
    "NetworkAttachment",
    "NetworkAttachmentModeChoices",
)


class NetworkAttachmentModeChoices(models.TextChoices):
    NETWORK = "network", "User defined network"
    NONE = "none", "None"
    HOST = "host", "Host"
    PRIVATE = "private", "Private"
    CUSTOM = "custom", "Custom"


class NetworkAttachment(NetBoxModel):
    container = models.ForeignKey(
        "netbox_containers.Container",
        on_delete=models.CASCADE,
        related_name="network_attachments",
        blank=True,
        null=True,
    )
    pod = models.ForeignKey(
        "netbox_containers.Pod",
        on_delete=models.CASCADE,
        related_name="network_attachments",
        blank=True,
        null=True,
    )
    mode = models.CharField(
        max_length=16,
        choices=NetworkAttachmentModeChoices.choices,
        default=NetworkAttachmentModeChoices.NETWORK,
    )
    network = models.ForeignKey(
        "netbox_containers.Network",
        on_delete=models.PROTECT,
        related_name="attachments",
        blank=True,
        null=True,
    )
    options = models.CharField(
        max_length=255,
        blank=True,
        help_text="Podman network options (e.g. pasta:--map-gw).",
    )

    class Meta:
        verbose_name = "Network Attachment"
        verbose_name_plural = "Network Attachments"
        ordering = ("pk",)

    def __str__(self):
        return self.spec

    @property
    def target(self):
        return self.container or self.pod

    @property
    def spec(self):
        if self.mode == NetworkAttachmentModeChoices.NETWORK and self.network:
            return str(self.network)
        return self.options or ""

    def clean(self):
        super().clean()
        if bool(self.container) == bool(self.pod):
            raise ValidationError("Exactly one of container or pod must be set.")
        if self.mode == NetworkAttachmentModeChoices.NETWORK:
            if not self.network:
                raise ValidationError({"network": "Network must be set for network mode."})
            if self.options:
                raise ValidationError({"options": "Options must be empty for network mode."})
        if self.mode == NetworkAttachmentModeChoices.CUSTOM:
            if not self.options:
                raise ValidationError({"options": "Options must be set for options mode."})
            if self.network:
                raise ValidationError({"network": "Network must be empty for options mode."})
        if self.mode in (NetworkAttachmentModeChoices.NONE, NetworkAttachmentModeChoices.HOST, NetworkAttachmentModeChoices.PRIVATE):
            if self.network:
                raise ValidationError({"network": "Network must be empty for this mode."})
            if self.options:
                raise ValidationError({"options": "Options must be empty for this mode."})

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:networkattachment", args=[self.pk])
