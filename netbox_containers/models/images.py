from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from netbox.models import NetBoxModel
from netbox_containers.constants import ImageArchChoices, ImageOSChoices


__all__ = (
    "Image",
    "ImageTag"
)


_registry_validator = RegexValidator(
    regex=r"^[a-z0-9][a-z0-9.-]*(:\d+)?$",
    message="Registry must be a hostname (optionally with port). Example: registry-1.docker.io or quay.io"
)


class Image(NetBoxModel):
    registry = models.CharField(max_length=255, validators=[_registry_validator], help_text="e.g. quay.io")
    name     = models.CharField(max_length=255, help_text="e.g. keycloak/keycloak")
    default_tag = models.CharField(max_length=128, blank=True, default="latest")
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ("registry", "name", "pk")
        constraints = [
            models.UniqueConstraint(fields=["registry", "name"], name="uniq_image_registry_name")
        ]

    def __str__(self):
        return f"{self.registry}/{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:image", args=[self.pk])

    @property
    def reference(self):
        # repo/name (no tag)
        return f"{self.registry}/{self.name}"


class ImageTag(NetBoxModel):
    image   = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="image_tags")
    image_tag = models.CharField(max_length=128, blank=True, default="latest")
    os      = models.CharField(max_length=32, choices=ImageOSChoices, blank=True)
    arch    = models.CharField(max_length=32, choices=ImageArchChoices, blank=True)
    digest  = models.CharField(max_length=128, blank=True, help_text="sha256:… (optional)")
    size    = models.BigIntegerField(blank=True, null=True, help_text="bytes (optional)")
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ("image__registry", "image__name", "image_tag", "arch", "os", "digest", "size", "pk")
        constraints = [
            models.UniqueConstraint(
                fields=["image", "image_tag", "os", "arch"],
                name="uniq_imagetag_variants_per_image",
            )
        ]
        verbose_name = "Image Tag"
        verbose_name_plural = "Image Tags"

    def __str__(self):
        suffix = []
        if self.os: suffix.append(self.os)
        if self.arch: suffix.append(self.arch)
        va = f" ({'/'.join(suffix)})" if suffix else ""
        return f"{self.image.reference}:{self.image_tag}{va}"

    @property
    def full_reference(self):
        # Includes tag
        return f"{self.image.reference}:{self.image_tag or 'latest'}"
