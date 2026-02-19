from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="add_group",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="One group per line: group name or gid (maps to --add-group).",
            ),
        ),
    ]
