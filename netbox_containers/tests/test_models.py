from django.test import TestCase
from netbox_containers.models import (
    Container,
    Pod,
    Network,
    NetworkAttachment,
    NetworkAttachmentModeChoices,
    Secret,
    ContainerSecret,
    ContainerSecretTypeChoices,
)


class NetworkAttachmentTests(TestCase):
    def test_network_attachment_requires_one_target(self):
        net = Network.objects.create(name="n1", driver="bridge")
        att = NetworkAttachment(network=net, mode=NetworkAttachmentModeChoices.NETWORK)
        with self.assertRaises(Exception):
            att.full_clean()

    def test_network_attachment_network_mode(self):
        net = Network.objects.create(name="n1", driver="bridge")
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(container=container, network=net, mode=NetworkAttachmentModeChoices.NETWORK)
        att.full_clean()

    def test_network_attachment_custom_mode(self):
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(container=container, mode=NetworkAttachmentModeChoices.CUSTOM, options="pasta:--map-gw")
        att.full_clean()


class ContainerSecretTests(TestCase):
    def test_env_secret_disallows_uid_gid_mode(self):
        container = Container.objects.create(name="c1", status="running")
        secret = Secret.objects.create(name="s1", driver="file")
        cs = ContainerSecret(
            container=container,
            secret=secret,
            type=ContainerSecretTypeChoices.ENV,
            target="ENV_VAR",
            uid=1000,
        )
        with self.assertRaises(Exception):
            cs.full_clean()

    def test_mount_secret_allows_uid_gid_mode(self):
        container = Container.objects.create(name="c1", status="running")
        secret = Secret.objects.create(name="s1", driver="file")
        cs = ContainerSecret(
            container=container,
            secret=secret,
            type=ContainerSecretTypeChoices.MOUNT,
            target="/run/secret",
            uid=1000,
            gid=1000,
            mode="0400",
        )
        cs.full_clean()
