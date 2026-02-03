from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


__all__ = (
    "Secret",
    "SecretDriverChoices",
)


class SecretDriverChoices(models.TextChoices):
    FILE = "file", "File"
    PASS = "pass", "Pass"
    SHELL = "shell", "Shell"


class Secret(NetBoxModel):
    name = models.CharField(max_length=100)
    driver = models.CharField(
        max_length=20,
        choices=SecretDriverChoices.choices,
    )
    options = models.TextField(
        blank=True,
        help_text="One option per line.",
    )

    class Meta:
        verbose_name = "Secret"
        verbose_name_plural = "Secrets"
        ordering = ("name", "pk")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_containers:secret", args=[self.pk])
