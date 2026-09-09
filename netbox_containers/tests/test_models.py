from django.core.exceptions import ValidationError
from django.test import TestCase

from netbox_containers.models import (
    Container,
    ContainerSecret,
    ContainerSecretTypeChoices,
    Image,
    ImageTag,
    Mount,
    Network,
    NetworkAttachment,
    NetworkAttachmentModeChoices,
    Pod,
    Secret,
    Volume,
)
from netbox_containers.models.mounts import MountTypeChoices


class ContainerTests(TestCase):
    def test_str_and_absolute_url(self):
        container = Container.objects.create(name="c1", status="running")
        self.assertEqual(str(container), "c1")
        self.assertEqual(
            container.get_absolute_url(),
            f"/plugins/netbox-containers/containers/{container.pk}/",
        )

    def test_get_status_color(self):
        container = Container.objects.create(name="c1", status="running")
        self.assertEqual(container.get_status_color(), "green")


class PodTests(TestCase):
    def test_infra_container_must_be_marked_infra(self):
        pod = Pod.objects.create(name="p1", status="running")
        container = Container.objects.create(name="c1", status="running", pod=pod)
        pod.infra_container = container
        with self.assertRaises(ValidationError):
            pod.full_clean()

    def test_infra_container_must_belong_to_pod(self):
        pod = Pod.objects.create(name="p1", status="running")
        other_pod = Pod.objects.create(name="p2", status="running")
        container = Container.objects.create(
            name="c1", status="running", pod=other_pod, is_infra=True
        )
        pod.infra_container = container
        with self.assertRaises(ValidationError):
            pod.full_clean()

    def test_valid_infra_container(self):
        pod = Pod.objects.create(name="p1", status="running")
        container = Container.objects.create(
            name="c1", status="running", pod=pod, is_infra=True
        )
        pod.infra_container = container
        pod.full_clean()


class NetworkTests(TestCase):
    def test_str_and_absolute_url(self):
        net = Network.objects.create(name="n1", driver="bridge")
        self.assertEqual(str(net), "n1")
        self.assertEqual(
            net.get_absolute_url(), f"/plugins/netbox-containers/networks/{net.pk}/"
        )

    def test_subnets_text_normalized_to_canonical_cidr(self):
        net = Network(name="n1", driver="bridge", subnets_text=["10.0.0.5/24"])
        net.full_clean()
        self.assertEqual(net.subnets_text, ["10.0.0.0/24"])

    def test_subnets_text_rejects_invalid_cidr(self):
        net = Network(name="n1", driver="bridge", subnets_text=["not-a-cidr"])
        with self.assertRaises(ValidationError):
            net.full_clean()

    def test_effective_subnets_combines_prefixes_and_text(self):
        net = Network.objects.create(
            name="n1", driver="bridge", subnets_text=["192.0.2.0/24"]
        )
        self.assertEqual(net.effective_subnets, ["192.0.2.0/24"])


class MountTests(TestCase):
    def test_volume_mount_requires_volume(self):
        container = Container.objects.create(name="c1", status="running")
        mount = Mount(
            container=container,
            mount_type=MountTypeChoices.VOLUME,
            dest_path="/data",
        )
        with self.assertRaises(ValidationError):
            mount.full_clean()

    def test_volume_mount_rejects_host_path(self):
        container = Container.objects.create(name="c1", status="running")
        volume = Volume.objects.create(name="v1", driver="local")
        mount = Mount(
            container=container,
            mount_type=MountTypeChoices.VOLUME,
            volume=volume,
            host_path="/srv/data",
            dest_path="/data",
        )
        with self.assertRaises(ValidationError):
            mount.full_clean()

    def test_bind_mount_requires_host_path(self):
        container = Container.objects.create(name="c1", status="running")
        mount = Mount(
            container=container,
            mount_type=MountTypeChoices.BIND,
            dest_path="/data",
        )
        with self.assertRaises(ValidationError):
            mount.full_clean()

    def test_bind_mount_rejects_volume(self):
        container = Container.objects.create(name="c1", status="running")
        volume = Volume.objects.create(name="v1", driver="local")
        mount = Mount(
            container=container,
            mount_type=MountTypeChoices.BIND,
            volume=volume,
            host_path="/srv/data",
            dest_path="/data",
        )
        with self.assertRaises(ValidationError):
            mount.full_clean()

    def test_valid_volume_mount_spec(self):
        container = Container.objects.create(name="c1", status="running")
        volume = Volume.objects.create(name="v1", driver="local")
        mount = Mount(
            container=container,
            mount_type=MountTypeChoices.VOLUME,
            volume=volume,
            dest_path="/data",
            options="ro",
        )
        mount.full_clean()
        self.assertEqual(mount.source, "v1")
        self.assertEqual(mount.spec, "v1:/data:ro")


class ImageTests(TestCase):
    def test_reference_and_full_reference(self):
        image = Image.objects.create(registry="quay.io", name="acme/app")
        tag = ImageTag.objects.create(image=image, image_tag="1.0")
        self.assertEqual(image.reference, "quay.io/acme/app")
        self.assertEqual(tag.full_reference, "quay.io/acme/app:1.0")

    def test_registry_and_name_must_be_unique_together(self):
        Image.objects.create(registry="quay.io", name="acme/app")
        with self.assertRaises(ValidationError):
            dup = Image(registry="quay.io", name="acme/app")
            dup.full_clean()


class NetworkAttachmentTests(TestCase):
    def test_network_attachment_requires_one_target(self):
        net = Network.objects.create(name="n1", driver="bridge")
        att = NetworkAttachment(network=net, mode=NetworkAttachmentModeChoices.NETWORK)
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_network_attachment_rejects_both_targets(self):
        net = Network.objects.create(name="n1", driver="bridge")
        container = Container.objects.create(name="c1", status="running")
        pod = Pod.objects.create(name="p1", status="running")
        att = NetworkAttachment(
            container=container,
            pod=pod,
            network=net,
            mode=NetworkAttachmentModeChoices.NETWORK,
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_network_attachment_network_mode(self):
        net = Network.objects.create(name="n1", driver="bridge")
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(
            container=container, network=net, mode=NetworkAttachmentModeChoices.NETWORK
        )
        att.full_clean()

    def test_network_attachment_network_mode_requires_network(self):
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(
            container=container, mode=NetworkAttachmentModeChoices.NETWORK
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_network_attachment_custom_mode(self):
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(
            container=container,
            mode=NetworkAttachmentModeChoices.CUSTOM,
            options="pasta:--map-gw",
        )
        att.full_clean()

    def test_network_attachment_custom_mode_requires_options(self):
        container = Container.objects.create(name="c1", status="running")
        att = NetworkAttachment(
            container=container, mode=NetworkAttachmentModeChoices.CUSTOM
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_network_attachment_none_mode_rejects_network_and_options(self):
        container = Container.objects.create(name="c1", status="running")
        net = Network.objects.create(name="n1", driver="bridge")
        att = NetworkAttachment(
            container=container,
            network=net,
            mode=NetworkAttachmentModeChoices.NONE,
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_network_attachment_host_mode(self):
        pod = Pod.objects.create(name="p1", status="running")
        att = NetworkAttachment(pod=pod, mode=NetworkAttachmentModeChoices.HOST)
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
        with self.assertRaises(ValidationError):
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
