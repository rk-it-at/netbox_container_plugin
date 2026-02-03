from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0031_published_ports_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="pod",
            name="add_host",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="One entry per line: HOSTNAME:IP (e.g. db:10.0.0.10)",
            ),
        ),
    ]
