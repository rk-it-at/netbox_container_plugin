import django_filters as filters
from django_filters import CharFilter, ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Mount


__all__ = (
    "MountFilterSet",
)


class MountFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')
    container_id = filters.NumberFilter(field_name="container_id")
    volume_id = filters.NumberFilter(field_name="volume_id")
    mount_type = filters.CharFilter()

    class Meta:
        model = Mount
        fields = (
            "id",
            "container_id",
            "mount_type",
            "volume_id",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(dest_path__icontains=value)
