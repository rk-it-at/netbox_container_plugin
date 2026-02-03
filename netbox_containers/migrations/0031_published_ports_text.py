from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0030_container_secret"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="published_ports",
            field=models.TextField(
                blank=True,
                help_text="One mapping per line: host_port:container_port (e.g. 8080:80).",
            ),
        ),
        migrations.AlterField(
            model_name="pod",
            name="published_ports",
            field=models.TextField(
                blank=True,
                help_text="One mapping per line: host_port:container_port (e.g. 8080:80).",
            ),
        ),
    ]
