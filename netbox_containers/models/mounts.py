from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from netbox.models import NetBoxModel


__all__ = (
    "Mount",
)

mount_opts_validator = RegexValidator(
    regex=r"^[A-Za-z0-9=,_:+.\-]*$",
    message="Options must be a comma-separated list (e.g. ro,Z,rshared,uid=1000).",
)

container_path_validator = RegexValidator(
    regex=r"^/.*",
    message="Destination path must be an absolute path inside the container (e.g. /var/lib/pgsql/data).",
)


class MountTypeChoices(models.TextChoices):
    VOLUME = "volume", "Named volume"
    BIND   = "bind",   "Host path (bind mount)"


class Mount(NetBoxModel):
    container = models.ForeignKey(
        "netbox_containers.Container",
        on_delete=models.CASCADE,
        related_name="mounts",
    )

    mount_type = models.CharField(
        max_length=16,
        choices=MountTypeChoices.choices,
        default=MountTypeChoices.VOLUME,
    )

    # Source can be either a Volume FK or a host path string, depending on mount_type
    volume = models.ForeignKey(
        "netbox_containers.Volume",
        on_delete=models.PROTECT,
        related_name="mounts",
        blank=True,
        null=True,
    )

    host_path = models.CharField(
        max_length=512,
        blank=True,
        help_text="Absolute host path (e.g. /srv/pgdata). Only for bind mounts.",
    )

    dest_path = models.CharField(
        max_length=512,
        validators=[container_path_validator],
        help_text="Destination path inside container (e.g. /var/lib/pgsql/data).",
    )

    options = models.CharField(
        max_length=255,
        blank=True,
        validators=[mount_opts_validator],
        help_text="Comma-separated mount options (e.g. ro,Z,rshared,uid=1000).",
    )


    class Meta:
        verbose_name = "Mount"
        verbose_name_plural = "Mounts"
        ordering = ("container_id", "pk")

    def __str__(self):
        return self.spec

    def clean(self):
        # Enforce mutual exclusivity between volume and host_path
        from django.core.exceptions import ValidationError

        if self.mount_type == MountTypeChoices.VOLUME:
            if not self.volume:
                raise ValidationError({"volume": "A named volume must be selected for volume mounts."})
            if self.host_path:
                raise ValidationError({"host_path": "Host path must be empty for volume mounts."})

        if self.mount_type == MountTypeChoices.BIND:
            if not self.host_path:
                raise ValidationError({"host_path": "Host path is required for bind mounts."})
            if self.volume_id:
                raise ValidationError({"volume": "Volume must be empty for bind mounts."})
            if not self.host_path.startswith("/"):
                raise ValidationError({"host_path": "Host path must be an absolute path."})

        super().clean()

    @property
    def source(self):
        return self.volume.name if self.mount_type == MountTypeChoices.VOLUME else self.host_path

    @property
    def spec(self):
        # Build podman -v spec: SRC:DEST[:OPTS]
        opts = (self.options or "").strip()
        base = f"{self.source}:{self.dest_path}"
        return f"{base}:{opts}" if opts else base

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:mount", args=[self.pk])
