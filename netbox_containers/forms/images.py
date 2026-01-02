from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from netbox_containers.models import Image, ImageTag
from netbox_containers.filtersets import ImageFilterSet, ImageTagFilterSet


__all__ = (
    "ImageForm",
    "ImageTagForm",
    "ImageFilterForm",
    "ImageTagFilterForm",
    "ImageBulkEditForm",
)


class ImageForm(NetBoxModelForm):
    comments = CommentField(required=False)

    class Meta:
        model = Image
        fields = [
            "name",
            "registry",
            "default_tag",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImageTagForm(NetBoxModelForm):
    image = DynamicModelChoiceField(queryset=Image.objects.all(), required=True)
    comments = CommentField(required=False)

    class Meta:
        model = ImageTag
        fields = (
            "image",
            "image_tag",
            "os",
            "arch",
            "digest",
            "size",
            "tags",
            "comments",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImageBulkEditForm(NetBoxModelBulkEditForm):
    model = Image

    registry = forms.CharField(required=False)
    label = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "registry",
            "label",
            name=_("Image"),
        ),
    )

    nullable_fields = ("os", "arch", "digest", "size", "label", "comments")       


class ImageFilterForm(NetBoxModelFilterSetForm):
    model = Image

    q = forms.CharField(required=False, label="Search")

    registry = forms.CharField(required=False, label=_("Registry"))
    name = forms.CharField(required=False, label=_("Name"))
    tag_label = forms.CharField(required=False, label=_("Tag (text search)"))

    fieldsets = (
        FieldSet("q", "registry", "name", "tag_label", name=_("Images")),
    )


class ImageTagFilterForm(NetBoxModelFilterSetForm):
    model = ImageTag

    q = forms.CharField(required=False, label=_("Search"))
    image = DynamicModelChoiceField(queryset=Image.objects.all(), required=False, label=_("Image"))
    image_tag = forms.CharField(required=False, label=_("Tag"))
    os = forms.CharField(required=False, label=_("OS"))
    arch = forms.CharField(required=False, label=_("Arch"))
    digest = forms.CharField(required=False, label=_("Digest"))

    fieldsets = (
        FieldSet("q", "image", "image_tag", "os", "arch", "digest", name=_("Image Tags")),
    )
