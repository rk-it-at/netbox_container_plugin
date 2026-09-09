from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class DetailViewRenderTests(TestCase):
    """Smoke tests: every detail/list page must render without error.

    These exercise the real templates (Tags/Comments includes, the
    render_table sub-tables, the checkmark/get_status_color markup) rather
    than a stand-in Django app, so they catch template bugs the unit tests
    below cannot.
    """

    @classmethod
    def setUpTestData(cls):
        cls.pod = Pod.objects.create(name="pod1", status="running")
        cls.container = Container.objects.create(
            name="c1", status="running", pod=cls.pod, is_infra=True
        )
        cls.pod.infra_container = cls.container
        cls.pod.save()

        cls.network = Network.objects.create(name="net1", driver="bridge")
        cls.image = Image.objects.create(registry="quay.io", name="acme/app")
        cls.image_tag = ImageTag.objects.create(image=cls.image, image_tag="1.0")
        cls.volume = Volume.objects.create(name="vol1", driver="local")
        cls.secret = Secret.objects.create(name="sec1", driver="file")
        cls.mount = Mount.objects.create(
            container=cls.container,
            mount_type=MountTypeChoices.VOLUME,
            volume=cls.volume,
            dest_path="/data",
        )
        cls.container_secret = ContainerSecret.objects.create(
            container=cls.container,
            secret=cls.secret,
            type=ContainerSecretTypeChoices.ENV,
            target="ENV_VAR",
        )
        cls.attachment = NetworkAttachment.objects.create(
            container=cls.container,
            network=cls.network,
            mode=NetworkAttachmentModeChoices.NETWORK,
        )

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username="tester", email="tester@example.com", password="pw"
        )
        self.client.force_login(self.user)

    def assertPageOK(self, viewname, kwargs=None):
        url = reverse(f"plugins:netbox_containers:{viewname}", kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            f"{viewname} ({url}) returned {response.status_code}",
        )

    def test_container_detail_and_list(self):
        self.assertPageOK("container", {"pk": self.container.pk})
        self.assertPageOK("container_list")

    def test_pod_detail_and_list(self):
        self.assertPageOK("pod", {"pk": self.pod.pk})
        self.assertPageOK("pod_list")

    def test_network_detail_and_list(self):
        self.assertPageOK("network", {"pk": self.network.pk})
        self.assertPageOK("network_list")

    def test_image_detail_and_list(self):
        self.assertPageOK("image", {"pk": self.image.pk})
        self.assertPageOK("image_list")

    def test_imagetag_detail_and_list(self):
        self.assertPageOK("imagetag", {"pk": self.image_tag.pk})
        self.assertPageOK("imagetag_list")

    def test_volume_detail_and_list(self):
        self.assertPageOK("volume", {"pk": self.volume.pk})
        self.assertPageOK("volume_list")

    def test_secret_detail_and_list(self):
        self.assertPageOK("secret", {"pk": self.secret.pk})
        self.assertPageOK("secret_list")

    def test_mount_detail_and_list(self):
        self.assertPageOK("mount", {"pk": self.mount.pk})
        self.assertPageOK("mount_list")

    def test_containersecret_detail_and_list(self):
        self.assertPageOK("containersecret", {"pk": self.container_secret.pk})
        self.assertPageOK("containersecret_list")

    def test_networkattachment_detail_and_list(self):
        self.assertPageOK("networkattachment", {"pk": self.attachment.pk})
        self.assertPageOK("networkattachment_list")

    def test_container_mounts_and_secrets_and_networks_tabs(self):
        self.assertPageOK("container_mounts", {"pk": self.container.pk})
        self.assertPageOK("container_secrets", {"pk": self.container.pk})
        self.assertPageOK("container_network_attachments", {"pk": self.container.pk})

    def test_pod_network_attachments_tab(self):
        self.assertPageOK("pod_network_attachments", {"pk": self.pod.pk})

    def test_empty_container_detail_renders(self):
        """A container with no mounts/secrets/networks/devices/VMs at all."""
        empty = Container.objects.create(name="empty", status="created")
        self.assertPageOK("container", {"pk": empty.pk})

    def test_empty_network_detail_renders(self):
        empty = Network.objects.create(name="empty-net", driver="bridge")
        self.assertPageOK("network", {"pk": empty.pk})

    def test_empty_pod_detail_renders(self):
        empty = Pod.objects.create(name="empty-pod", status="created")
        self.assertPageOK("pod", {"pk": empty.pk})


class AddFromParentViewTests(TestCase):
    """The "Add Components" flows that inject a parent id via the URL."""

    @classmethod
    def setUpTestData(cls):
        cls.container = Container.objects.create(name="c1", status="running")
        cls.pod = Pod.objects.create(name="p1", status="running")
        cls.volume = Volume.objects.create(name="v1", driver="local")
        cls.secret = Secret.objects.create(name="s1", driver="file")
        cls.network = Network.objects.create(name="n1", driver="bridge")

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username="tester2", email="tester2@example.com", password="pw"
        )
        self.client.force_login(self.user)

    def test_add_mount_from_container_prefills_container(self):
        url = reverse(
            "plugins:netbox_containers:mount_add_from_container",
            kwargs={"container_id": self.container.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "mount_type": MountTypeChoices.VOLUME,
                "volume": self.volume.pk,
                "dest_path": "/data",
                "options": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        mount = Mount.objects.get(dest_path="/data")
        self.assertEqual(mount.container_id, self.container.pk)

    def test_add_secret_from_container_prefills_container(self):
        url = reverse(
            "plugins:netbox_containers:containersecret_add_from_container",
            kwargs={"container_id": self.container.pk},
        )
        response = self.client.post(
            url,
            {
                "secret": self.secret.pk,
                "type": ContainerSecretTypeChoices.ENV,
                "target": "ENV_VAR",
            },
        )
        self.assertEqual(response.status_code, 302)
        cs = ContainerSecret.objects.get(target="ENV_VAR")
        self.assertEqual(cs.container_id, self.container.pk)

    def test_add_network_attachment_from_container_prefills_container(self):
        url = reverse(
            "plugins:netbox_containers:network_attachment_add_from_container",
            kwargs={"container_id": self.container.pk},
        )
        response = self.client.post(
            url,
            {
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": self.network.pk,
                "options": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        att = NetworkAttachment.objects.get(network=self.network)
        self.assertEqual(att.container_id, self.container.pk)
        self.assertIsNone(att.pod_id)

    def test_add_network_attachment_from_pod_prefills_pod(self):
        url = reverse(
            "plugins:netbox_containers:network_attachment_add_from_pod",
            kwargs={"pod_id": self.pod.pk},
        )
        response = self.client.post(
            url,
            {
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": self.network.pk,
                "options": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        att = NetworkAttachment.objects.get(network=self.network)
        self.assertEqual(att.pod_id, self.pod.pk)
        self.assertIsNone(att.container_id)
