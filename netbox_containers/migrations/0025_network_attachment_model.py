from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0024_container_is_infra_pod_infra_container"),
    ]

    operations = [
        migrations.CreateModel(
            name="NetworkAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("mode", models.CharField(choices=[("network", "Network"), ("options", "Options")], default="network", max_length=16)),
                ("options", models.CharField(blank=True, help_text="Podman network options (e.g. pasta:--map-gw).", max_length=255)),
                ("container", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="network_attachments", to="netbox_containers.container")),
                ("network", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="attachments", to="netbox_containers.network")),
                ("pod", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="network_attachments", to="netbox_containers.pod")),
            ],
            options={
                "verbose_name": "Network Attachment",
                "verbose_name_plural": "Network Attachments",
                "ordering": ("pk",),
            },
        ),
    ]
