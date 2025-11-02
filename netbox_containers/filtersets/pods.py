import django_filters as filters
from django_filters import CharFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Pod


__all__ = (
    "PodFilterSet",
)


class PodFilterSet(NetBoxModelFilterSet):
    q = CharFilter(method='search', label='Search')

    status = filters.MultipleChoiceFilter(
        choices=Pod._meta.get_field("status").choices
    )

    class Meta:
        model = Pod
        fields = (
            "id",
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "tag"
        )

    def search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
