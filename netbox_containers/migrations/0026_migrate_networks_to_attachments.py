from django.db import migrations


def forward(apps, schema_editor):
    Container = apps.get_model("netbox_containers", "Container")
    Pod = apps.get_model("netbox_containers", "Pod")
    NetworkAttachment = apps.get_model("netbox_containers", "NetworkAttachment")

    attachments = []
    for container in Container.objects.all():
        for network in container.networks.all():
            attachments.append(NetworkAttachment(
                container_id=container.pk,
                mode="network",
                network_id=network.pk,
            ))

    for pod in Pod.objects.all():
        for network in pod.networks.all():
            attachments.append(NetworkAttachment(
                pod_id=pod.pk,
                mode="network",
                network_id=network.pk,
            ))

    if attachments:
        NetworkAttachment.objects.bulk_create(attachments)


def backward(apps, schema_editor):
    NetworkAttachment = apps.get_model("netbox_containers", "NetworkAttachment")
    NetworkAttachment.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_containers", "0025_network_attachment_model"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
