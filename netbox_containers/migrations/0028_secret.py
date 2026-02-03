from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0027_remove_networks_from_container_pod"),
    ]

    operations = [
        migrations.CreateModel(
            name="Secret",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=100)),
                ("driver", models.CharField(choices=[("file", "File"), ("pass", "Pass"), ("shell", "Shell")], max_length=20)),
                ("options", models.JSONField(blank=True, default=dict, help_text="Driver options (JSON object).")),
            ],
            options={
                "verbose_name": "Secret",
                "verbose_name_plural": "Secrets",
                "ordering": ("name", "pk"),
            },
        ),
    ]
