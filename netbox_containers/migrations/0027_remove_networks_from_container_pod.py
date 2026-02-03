from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0026_migrate_networks_to_attachments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="container",
            name="networks",
        ),
        migrations.RemoveField(
            model_name="pod",
            name="networks",
        ),
    ]
