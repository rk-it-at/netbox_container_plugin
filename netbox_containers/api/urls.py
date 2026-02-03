from netbox.api.routers import NetBoxRouter

from . import views


app_name = "netbox_containers"

router = NetBoxRouter()
router.APIRootView = views.ContainersRootView
router.register("pods", views.PodViewSet)
router.register("networks", views.NetworkViewSet)
router.register("images", views.ImageViewSet)
router.register("imagetags", views.ImageTagViewSet)
router.register("volumes", views.VolumeViewSet)
router.register("containers", views.ContainerViewSet)
router.register("mounts", views.MountViewSet)
router.register("network-attachments", views.NetworkAttachmentViewSet)
router.register("secrets", views.SecretViewSet)
router.register("container-secrets", views.ContainerSecretViewSet)

urlpatterns = router.urls
