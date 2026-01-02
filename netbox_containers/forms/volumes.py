from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from netbox_containers.models import Volume


__all__ = (
    "VolumeForm",
    "VolumeFilterForm",
    "VolumeBulkEditForm",
)


class VolumeForm(NetBoxModelForm):
    comments = CommentField(required=False)

    class Meta:
        model = Volume
        fields = [
            "name",
            "driver",
            "label",
            "options",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = Volume

    driver = forms.CharField(required=False)
    label = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "driver",
            "label",
            name=_("Volume"),
        ),
    )

    nullable_fields = ("options", "comments")  


class VolumeFilterForm(NetBoxModelFilterSetForm):
    model = Volume

    q = forms.CharField(required=False, label="Search")

    driver = forms.ChoiceField(
        choices=Volume._meta.get_field("driver").choices,
        required=False,
        label=_("Driver"),
    )

    fieldsets = (
        FieldSet("q", "driver", name=_("Volumes")),
    )
