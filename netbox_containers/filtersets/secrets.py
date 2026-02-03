import django_filters as filters
from django_filters import CharFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Secret


__all__ = (
    "SecretFilterSet",
)


class SecretFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method="search", label="Search")
    driver = filters.MultipleChoiceFilter(
        choices=Secret._meta.get_field("driver").choices
    )

    class Meta:
        model = Secret
        fields = (
            "id",
            "name",
            "driver",
            "tag",
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
