from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0023_remove_container_volumes_mount"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="is_infra",
            field=models.BooleanField(
                default=False,
                help_text="Mark this container as the infra container for a pod.",
            ),
        ),
        migrations.AddField(
            model_name="pod",
            name="infra_container",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="infra_for_pods",
                to="netbox_containers.container",
            ),
        ),
    ]
