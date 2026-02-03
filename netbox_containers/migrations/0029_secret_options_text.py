from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0028_secret"),
    ]

    operations = [
        migrations.AlterField(
            model_name="secret",
            name="options",
            field=models.TextField(blank=True, help_text="One option per line."),
        ),
    ]
