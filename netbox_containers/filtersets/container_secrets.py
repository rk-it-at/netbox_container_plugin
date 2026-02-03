import django_filters as filters
from django_filters import CharFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import ContainerSecret


__all__ = (
    "ContainerSecretFilterSet",
)


class ContainerSecretFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method="search", label="Search")
    container_id = filters.NumberFilter(field_name="container_id")
    secret_id = filters.NumberFilter(field_name="secret_id")
    type = filters.CharFilter()

    class Meta:
        model = ContainerSecret
        fields = (
            "id",
            "container_id",
            "secret_id",
            "type",
            "tag",
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(target__icontains=value)
