from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0002_container_add_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="add_device",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="One device per line (maps to --device), e.g. /dev/ttyUSB0 or /dev/sda:/dev/xvda:rwm.",
            ),
        ),
    ]
