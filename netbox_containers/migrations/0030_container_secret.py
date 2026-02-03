from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0029_secret_options_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContainerSecret",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("type", models.CharField(choices=[("mount", "Mount"), ("env", "Env")], max_length=16)),
                ("target", models.CharField(help_text="Mount path or environment variable name.", max_length=255)),
                ("uid", models.PositiveIntegerField(blank=True, null=True)),
                ("gid", models.PositiveIntegerField(blank=True, null=True)),
                ("mode", models.CharField(blank=True, help_text="File mode (e.g. 0400). Only for mount.", max_length=8)),
                ("container", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="secrets", to="netbox_containers.container")),
                ("secret", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="container_secrets", to="netbox_containers.secret")),
            ],
            options={
                "verbose_name": "Container Secret",
                "verbose_name_plural": "Container Secrets",
                "ordering": ("container_id", "pk"),
            },
        ),
    ]
