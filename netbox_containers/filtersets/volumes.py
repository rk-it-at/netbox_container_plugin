import django_filters as filters
from django_filters import CharFilter, ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Volume


__all__ = (
    "VolumeFilterSet",
)


class VolumeFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')

    driver = filters.MultipleChoiceFilter(
        choices=Volume._meta.get_field("driver").choices
    )

    class Meta:
        model = Volume
        fields = (
            "id",
            "name",
            "driver",
            "label",
            "options",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
