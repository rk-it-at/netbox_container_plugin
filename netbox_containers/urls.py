from django.urls import include, path
from utilities.urls import get_model_urls
from . import views


def get_urls(model_name, url_prefix, *, pk="<int:pk>"):
    return (
        path(f"{url_prefix}/", include(get_model_urls("netbox_containers", model_name, detail=False))),
        path(f"{url_prefix}/{pk}/", include(get_model_urls("netbox_containers", model_name))),
    )


urlpatterns = (
    *get_urls("network", "networks"),
    *get_urls("pod", "pods"),
    *get_urls("image", "images"),
    *get_urls("imagetag", "imagetags"),
    *get_urls("volume", "volumes"),
    *get_urls("mount", "mounts"),
    *get_urls("networkattachment", "network-attachments"),
    *get_urls("secret", "secrets"),
    *get_urls("containersecret", "container-secrets"),
    *get_urls("container", "containers"),
    path(
        "network-attachments/containers/",
        views.NetworkAttachmentContainerListView.as_view(),
        name="networkattachment_container_list",
    ),
    path(
        "network-attachments/pods/",
        views.NetworkAttachmentPodListView.as_view(),
        name="networkattachment_pod_list",
    ),
    path(
        "containers/<int:container_id>/mounts/add/",
        views.MountCreateView.as_view(),
        name="mount_add_from_container",
    ),
    path(
        "containers/<int:container_id>/network-attachments/add/",
        views.NetworkAttachmentCreateView.as_view(),
        name="network_attachment_add_from_container",
    ),
    path(
        "pods/<int:pod_id>/network-attachments/add/",
        views.NetworkAttachmentCreateView.as_view(),
        name="network_attachment_add_from_pod",
    ),
    path(
        "containers/<int:container_id>/secrets/add/",
        views.ContainerSecretCreateView.as_view(),
        name="containersecret_add_from_container",
    ),
)
