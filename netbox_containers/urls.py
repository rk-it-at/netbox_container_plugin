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
)
