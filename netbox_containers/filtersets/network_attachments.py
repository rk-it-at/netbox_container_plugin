import django_filters as filters
from django_filters import CharFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import NetworkAttachment


__all__ = (
    "NetworkAttachmentFilterSet",
)


class NetworkAttachmentFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method="search", label="Search")
    container_id = filters.NumberFilter(field_name="container_id")
    pod_id = filters.NumberFilter(field_name="pod_id")
    network_id = filters.NumberFilter(field_name="network_id")
    mode = filters.CharFilter()

    class Meta:
        model = NetworkAttachment
        fields = (
            "id",
            "container_id",
            "pod_id",
            "network_id",
            "mode",
            "tag",
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(options__icontains=value)
