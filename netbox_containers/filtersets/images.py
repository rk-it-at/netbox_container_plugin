import django_filters as filters
from django_filters import CharFilter, ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from netbox_containers.models import Image, ImageTag


__all__ = (
    "ImageFilterSet",
    "ImageTagFilterSet",
)


class ImageFilterSet(NetBoxModelFilterSet):
    q = filters.CharFilter(method="search", label="Search")
    tag_label = filters.CharFilter(field_name="tags__name", lookup_expr="icontains")

    class Meta:
        model = Image
        fields = ("id", "registry", "name", "tag_label", "tag")

    def search(self, qs, name, value):
        if not value:
            return qs
        return qs.filter(name__icontains=value) | qs.filter(registry__icontains=value)


class ImageTagFilterSet(NetBoxModelFilterSet):
    q = filters.CharFilter(method="search", label="Search")
    image_id = filters.NumberFilter(field_name="image_id")

    class Meta:
        model = ImageTag
        fields = ("id", "image_id", "image_tag", "os", "arch", "digest", "tag")

    def search(self, qs, name, value):
        if not value:
            return qs
        return qs.filter(tag__icontains=value) | qs.filter(image__name__icontains=value)
