from django.test import TestCase

from netbox_containers.forms import (
    ContainerForm,
    ContainerSecretCreateForm,
    ContainerSecretEditForm,
    ContainerSecretForm,
    MountCreateForm,
    MountForm,
    NetworkAttachmentCreateForm,
    NetworkAttachmentEditForm,
    NetworkAttachmentForm,
)
from netbox_containers.models import (
    Container,
    ContainerSecret,
    ContainerSecretTypeChoices,
    Network,
    NetworkAttachment,
    NetworkAttachmentModeChoices,
    Pod,
    Secret,
    Volume,
)
from netbox_containers.models.mounts import MountTypeChoices


class ContainerFormLineListFieldTests(TestCase):
    def _base_data(self, **overrides):
        data = {
            "name": "c1",
            "status": "running",
            "add_host_text": "",
            "add_group_text": "",
            "add_device_text": "",
            "environment_text": "",
        }
        data.update(overrides)
        return data

    def test_valid_line_list_fields_parse_and_save(self):
        form = ContainerForm(
            data=self._base_data(
                add_host_text="db:10.0.0.10\ncache:10.0.0.20",
                environment_text="TZ=UTC\nDEBUG=1",
            )
        )
        self.assertTrue(form.is_valid(), form.errors)
        container = form.save()
        self.assertEqual(container.add_host, ["db:10.0.0.10", "cache:10.0.0.20"])
        self.assertEqual(container.environment, ["TZ=UTC", "DEBUG=1"])

    def test_invalid_add_host_entry_rejected(self):
        form = ContainerForm(data=self._base_data(add_host_text="not-a-hostip-pair"))
        self.assertFalse(form.is_valid())
        self.assertIn("add_host_text", form.errors)

    def test_invalid_environment_entry_rejected(self):
        form = ContainerForm(data=self._base_data(environment_text="NOT_KEY_VALUE"))
        self.assertFalse(form.is_valid())
        self.assertIn("environment_text", form.errors)

    def test_editing_prepopulates_line_list_fields_as_text(self):
        container = Container.objects.create(
            name="c2", status="running", add_host=["db:10.0.0.10"]
        )
        form = ContainerForm(instance=container)
        rendered = str(form["add_host_text"])
        self.assertIn("db:10.0.0.10", rendered)

    def test_image_tag_must_belong_to_selected_image(self):
        from netbox_containers.models import Image, ImageTag

        image = Image.objects.create(registry="quay.io", name="acme/app")
        other_image = Image.objects.create(registry="quay.io", name="acme/other")
        tag = ImageTag.objects.create(image=other_image, image_tag="1.0")

        form = ContainerForm(data=self._base_data(image=image.pk, image_tag=tag.pk))
        self.assertFalse(form.is_valid())


class MountFormTests(TestCase):
    def setUp(self):
        self.container = Container.objects.create(name="c1", status="running")
        self.volume = Volume.objects.create(name="v1", driver="local")

    def test_volume_mount_requires_volume(self):
        form = MountForm(
            data={
                "container": self.container.pk,
                "mount_type": MountTypeChoices.VOLUME,
                "volume": "",
                "host_path": "",
                "dest_path": "/data",
                "options": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_bind_mount_requires_host_path(self):
        form = MountForm(
            data={
                "container": self.container.pk,
                "mount_type": MountTypeChoices.BIND,
                "volume": "",
                "host_path": "",
                "dest_path": "/data",
                "options": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_valid_volume_mount(self):
        form = MountForm(
            data={
                "container": self.container.pk,
                "mount_type": MountTypeChoices.VOLUME,
                "volume": self.volume.pk,
                "host_path": "",
                "dest_path": "/data",
                "options": "",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_create_form_injects_container_id(self):
        form = MountCreateForm(
            data={
                "mount_type": MountTypeChoices.VOLUME,
                "volume": self.volume.pk,
                "host_path": "",
                "dest_path": "/data2",
                "options": "",
            },
            container_id=self.container.pk,
        )
        self.assertTrue(form.is_valid(), form.errors)
        mount = form.save()
        self.assertEqual(mount.container_id, self.container.pk)


class NetworkAttachmentFormValidationTests(TestCase):
    """Cross-field validation now lives solely on the model; these confirm
    all three forms still surface it correctly."""

    def setUp(self):
        self.container = Container.objects.create(name="c1", status="running")
        self.pod = Pod.objects.create(name="p1", status="running")
        self.network = Network.objects.create(name="n1", driver="bridge")

    def test_full_form_rejects_neither_container_nor_pod(self):
        form = NetworkAttachmentForm(
            data={
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": self.network.pk,
                "options": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_full_form_accepts_valid_network_mode(self):
        form = NetworkAttachmentForm(
            data={
                "container": self.container.pk,
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": self.network.pk,
                "options": "",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_create_form_rejects_custom_mode_without_options(self):
        instance = NetworkAttachment(container_id=self.container.pk)
        form = NetworkAttachmentCreateForm(
            data={
                "mode": NetworkAttachmentModeChoices.CUSTOM,
                "network": "",
                "options": "",
            },
            instance=instance,
            container_id=self.container.pk,
        )
        self.assertFalse(form.is_valid())

    def test_create_form_accepts_valid_custom_mode(self):
        instance = NetworkAttachment(container_id=self.container.pk)
        form = NetworkAttachmentCreateForm(
            data={
                "mode": NetworkAttachmentModeChoices.CUSTOM,
                "network": "",
                "options": "pasta:--map-gw",
            },
            instance=instance,
            container_id=self.container.pk,
        )
        self.assertTrue(form.is_valid(), form.errors)
        att = form.save()
        self.assertEqual(att.container_id, self.container.pk)

    def test_edit_form_rejects_network_mode_without_network(self):
        existing = NetworkAttachment.objects.create(
            pod=self.pod, mode=NetworkAttachmentModeChoices.HOST
        )
        form = NetworkAttachmentEditForm(
            data={
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": "",
                "options": "",
            },
            instance=existing,
        )
        self.assertFalse(form.is_valid())

    def test_edit_form_accepts_valid_change(self):
        existing = NetworkAttachment.objects.create(
            pod=self.pod, mode=NetworkAttachmentModeChoices.HOST
        )
        form = NetworkAttachmentEditForm(
            data={
                "mode": NetworkAttachmentModeChoices.NETWORK,
                "network": self.network.pk,
                "options": "",
            },
            instance=existing,
        )
        self.assertTrue(form.is_valid(), form.errors)


class ContainerSecretFormValidationTests(TestCase):
    def setUp(self):
        self.container = Container.objects.create(name="c1", status="running")
        self.secret = Secret.objects.create(name="s1", driver="file")

    def test_full_form_rejects_env_with_uid(self):
        form = ContainerSecretForm(
            data={
                "container": self.container.pk,
                "secret": self.secret.pk,
                "type": ContainerSecretTypeChoices.ENV,
                "target": "ENV_VAR",
                "uid": 1000,
                "gid": "",
                "mode": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_full_form_accepts_valid_env_secret(self):
        form = ContainerSecretForm(
            data={
                "container": self.container.pk,
                "secret": self.secret.pk,
                "type": ContainerSecretTypeChoices.ENV,
                "target": "ENV_VAR",
                "uid": "",
                "gid": "",
                "mode": "",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_create_form_rejects_env_with_mode(self):
        instance = ContainerSecret(container_id=self.container.pk)
        form = ContainerSecretCreateForm(
            data={
                "secret": self.secret.pk,
                "type": ContainerSecretTypeChoices.ENV,
                "target": "ENV_VAR",
                "uid": "",
                "gid": "",
                "mode": "0400",
            },
            instance=instance,
            container_id=self.container.pk,
        )
        self.assertFalse(form.is_valid())

    def test_edit_form_accepts_valid_mount_secret(self):
        existing = ContainerSecret.objects.create(
            container=self.container,
            secret=self.secret,
            type=ContainerSecretTypeChoices.MOUNT,
            target="/run/secret",
        )
        form = ContainerSecretEditForm(
            data={
                "secret": self.secret.pk,
                "type": ContainerSecretTypeChoices.MOUNT,
                "target": "/run/secret2",
                "uid": 1000,
                "gid": 1000,
                "mode": "0400",
            },
            instance=existing,
        )
        self.assertTrue(form.is_valid(), form.errors)
