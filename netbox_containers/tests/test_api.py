from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from netbox_containers.models import Container, Pod


class ContainerAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pod = Pod.objects.create(name="p1", status="running")
        cls.container = Container.objects.create(
            name="c1", status="running", pod=cls.pod
        )

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username="apitester", email="apitester@example.com", password="pw"
        )
        self.client.force_authenticate(user=self.user)

    def test_list_containers(self):
        url = reverse("plugins-api:netbox_containers-api:container-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_container(self):
        url = reverse(
            "plugins-api:netbox_containers-api:container-detail",
            kwargs={"pk": self.container.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "c1")

    def test_create_container(self):
        url = reverse("plugins-api:netbox_containers-api:container-list")
        response = self.client.post(
            url, {"name": "c2", "status": "running", "pod": self.pod.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(Container.objects.filter(name="c2").exists())

    def test_create_container_rejects_invalid_status(self):
        url = reverse("plugins-api:netbox_containers-api:container-list")
        response = self.client.post(url, {"name": "c3", "status": "not-a-status"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_containers_by_pod(self):
        other_pod = Pod.objects.create(name="p2", status="running")
        Container.objects.create(name="c-other", status="running", pod=other_pod)
        url = reverse("plugins-api:netbox_containers-api:container-list")
        response = self.client.get(url, {"pod_id": self.pod.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {c["name"] for c in response.data["results"]}
        self.assertEqual(names, {"c1"})


class OtherModelAPISmokeTests(APITestCase):
    """One list+create round trip per remaining ViewSet, to catch a broken
    serializer/router registration without a full test class each."""

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username="apitester2", email="apitester2@example.com", password="pw"
        )
        self.client.force_authenticate(user=self.user)

    def test_pod_list_and_create(self):
        list_url = reverse("plugins-api:netbox_containers-api:pod-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
        response = self.client.post(list_url, {"name": "pod1", "status": "running"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_network_list_and_create(self):
        list_url = reverse("plugins-api:netbox_containers-api:network-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
        response = self.client.post(list_url, {"name": "net1", "driver": "bridge"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_volume_list_and_create(self):
        list_url = reverse("plugins-api:netbox_containers-api:volume-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
        response = self.client.post(list_url, {"name": "vol1", "driver": "local"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_secret_list_and_create(self):
        list_url = reverse("plugins-api:netbox_containers-api:secret-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
        response = self.client.post(list_url, {"name": "sec1", "driver": "file"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_image_list_and_create(self):
        list_url = reverse("plugins-api:netbox_containers-api:image-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
        response = self.client.post(
            list_url, {"registry": "quay.io", "name": "acme/app"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_mount_list(self):
        list_url = reverse("plugins-api:netbox_containers-api:mount-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)

    def test_network_attachment_list(self):
        list_url = reverse("plugins-api:netbox_containers-api:networkattachment-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)

    def test_container_secret_list(self):
        list_url = reverse("plugins-api:netbox_containers-api:containersecret-list")
        self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
