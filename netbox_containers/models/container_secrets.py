from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


__all__ = (
    "ContainerSecret",
    "ContainerSecretTypeChoices",
)


class ContainerSecretTypeChoices(models.TextChoices):
    MOUNT = "mount", "Mount"
    ENV = "env", "Env"


class ContainerSecret(NetBoxModel):
    container = models.ForeignKey(
        "netbox_containers.Container",
        on_delete=models.CASCADE,
        related_name="secrets",
    )
    secret = models.ForeignKey(
        "netbox_containers.Secret",
        on_delete=models.PROTECT,
        related_name="container_secrets",
    )
    type = models.CharField(
        max_length=16,
        choices=ContainerSecretTypeChoices.choices,
    )
    target = models.CharField(
        max_length=255,
        help_text="Mount path or environment variable name.",
    )
    uid = models.PositiveIntegerField(blank=True, null=True)
    gid = models.PositiveIntegerField(blank=True, null=True)
    mode = models.CharField(
        max_length=8,
        blank=True,
        help_text="File mode (e.g. 0400). Only for mount.",
    )

    class Meta:
        verbose_name = "Container Secret"
        verbose_name_plural = "Container Secrets"
        ordering = ("container_id", "pk")

    def __str__(self):
        return f"{self.secret} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.type == ContainerSecretTypeChoices.ENV:
            if self.uid or self.gid or self.mode:
                raise ValidationError("UID/GID/Mode are only valid for mount secrets.")

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:containersecret", args=[self.pk])
