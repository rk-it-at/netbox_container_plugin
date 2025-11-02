from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, CommentField
from utilities.forms.rendering import FieldSet
from netbox_containers.models import Pod, Network
from netbox_containers.filtersets import PodFilterSet


__all__ = (
    "PodForm",
    "PodFilterForm",
    "PodBulkEditForm",
)


class PodForm(NetBoxModelForm):
    networks = DynamicModelMultipleChoiceField(
        queryset=Network.objects.all(),
        required=False,
        label="Networks",
    )
    comments = CommentField(required=False)

    class Meta:
        model = Pod
        fields = [
            "name",
            "status",
            "user",
            "published_ports",
            "networks",
            "tags",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PodBulkEditForm(NetBoxModelBulkEditForm):
    model = Pod

    user = forms.CharField(required=False)
    comments = CommentField(required=False)

    fieldsets = (
        FieldSet(
            "user",
            name=_("Pod"),
        ),
    )

    nullable_fields = ("user", "comments")  


class PodFilterForm(NetBoxModelFilterSetForm):
    model = Pod
    filterset_class = PodFilterSet
