from netbox.api.routers import NetBoxRouter

from . import views


app_name = "netbox_containers"

router = NetBoxRouter()
router.APIRootView = views.ContainersRootView
router.register("pods", views.PodViewSet)
router.register("networks", views.NetworkViewSet)

urlpatterns = router.urls
